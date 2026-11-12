import sys
from flask import render_template, flash, redirect, url_for, jsonify, request, flash, abort
from flask_login import current_user, login_required
import sqlalchemy as sqla

from app import db

from app.main.models import Booking, User, Machine, Location, Report, Review, Reservation
from app.main.forms import BookingForm, ReportForm, ReviewForm
from datetime import datetime, timedelta, timezone


from app.main import main_blueprint as bp_main

@bp_main.route('/profile', methods=['GET'])
@login_required
def profile():
    # Janky placeholder profile info
    profile_info = {
        "Username": current_user.username,
        "Email": getattr(current_user, "email", "Not set"),
        "Membership": "Regular",
        "Past Reservations": ["Machine #1 - 08:00", "Machine #3 - 10:00"],
        "Preferences": ["Eco Wash", "Extra Spin"]
    }

    if(current_user.user_type == "Admin"):
        reports = db.session.query(Report).filter(Report.machine.has(location_id=current_user.location_id)).all()
        return render_template('profile.html', title="Profile", profile_info=profile_info, reports=reports)
    elif(current_user.user_type == "User"):
        bulk_bookings = db.session.scalars(sqla.select(Booking).where(Booking.user_id == current_user.id)).all()
        reservations = db.session.scalars(sqla.select(Reservation).where(Reservation.user_id == current_user.id)).all()
        return render_template('profile.html', title="Profile", profile_info=profile_info, bulk_bookings=bulk_bookings, reservations=reservations)
    elif(current_user.user_type == "Driver"):
        bulk_bookings = Booking.query.filter(Booking.driver_id == current_user.id).all()
        return render_template('profile.html', title="Profile", profile_info=profile_info, bulk_bookings=bulk_bookings)
    return render_template('profile.html', title="Profile", profile_info=profile_info)


@bp_main.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def deletebooking(post_id):
    thebooking = db.session.get(Booking, post_id)

    if thebooking:

        db.session.delete(thebooking)
        db.session.commit()

        flash(f'Your "{thebooking.machine_type}" is no longer booked.')

    return redirect(url_for('main.map_page'))

@bp_main.route('/reserve_bulk/<int:location_id>', methods=['GET', 'POST'])
@login_required
def reserve_bulk(location_id):
    location = db.session.get(Location, location_id)
    form = BookingForm()
    if form.validate_on_submit():
        steps = ["Picked up"]
        if 'washer' in form.machine_type.data:
            steps.append("Washing")
        if 'dryer' in form.machine_type.data:
            steps.append("Drying")
        
        steps.append("Delivering")
        m_type = " and ".join(form.machine_type.data)
        booking = Booking(user_id=current_user.id,address=form.address.data,location_id=location_id, progress = steps, machine_type=m_type, start_time=datetime.now(timezone.utc))
        db.session.add(booking)
        db.session.commit()
        flash('Congratulations, your bulk booking has been confirmed!')
        return redirect(url_for('main.location', location_id=location_id))
    return render_template('reserve_bulk.html', title='Bulk Booking', form=form, location=location)

@bp_main.route('/booking/<int:booking_id>/complete_delivery', methods=['POST'])
@login_required
def complete_delivery(booking_id):
    booking = db.session.get(Booking, booking_id)
    if booking and booking.driver_id == current_user.id:
        if booking.status == "Delivering":
            db.session.delete(booking)
            db.session.commit()
            flash("Delivery Completed.", "info")
            return redirect(url_for('main.profile'))
        else:
            flash("Could not cancel reservation.", "danger")
            return redirect(url_for('main.map_page'))

@bp_main.route('/claim_booking/<int:booking_id>', methods=['POST'])
@login_required
def claim_booking(booking_id):
    booking = db.session.get(Booking, booking_id)
    booking.driver_id = current_user.id
    db.session.commit()
    flash(f"Booking #{booking.id} has been added to your profile!", "success")
    return redirect(url_for('main.profile'))

@bp_main.route('/status_update/<int:booking_id>', methods=['POST'])
@login_required
def status_update(booking_id):
    booking = db.session.get(Booking, booking_id)
    steps = booking.progress

        # Move to the next step in booking.steps
    steps = booking.progress
    current_index = steps.index(booking.status) if booking.status in steps else 0
    if current_index + 1 < len(steps):
        booking.status = steps[current_index + 1]
        db.session.commit()
    return redirect(url_for('main.profile'))

@bp_main.route('/claim_booking/<int:booking_id>', methods=['POST'])
@login_required
def status_view(booking_id):
    booking = db.session.get(Booking, booking_id)
    booking.user_id = current_user.id
    db.session.commit()
    flash(f"Booking #{booking.id} has been added to your profile!", "success")
    return redirect(url_for('main.profile'))

@bp_main.route('/reservation/<int:reservation_id>/cancel', methods=['POST'])
@login_required
def cancel_reservation(reservation_id):
    reservation = db.session.get(Reservation, reservation_id)
    if reservation and reservation.user_id == current_user.id:
        location_id = reservation.machine.location_id
        db.session.delete(reservation)
        db.session.commit()
        flash("Reservation cancelled.", "info")
        return redirect(url_for('main.location', location_id=location_id))
    flash("Could not cancel reservation.", "danger")
    return redirect(url_for('main.map_page'))


@bp_main.route('/')
@bp_main.route('/map')
@login_required
def map_page():
    locations = db.session.scalars(sqla.select(Location)).all()
    return render_template(
        "map_page.html",
        title="Laundry Map",
        locations=locations
    )

@bp_main.route('/location/<int:location_id>')
@login_required
def location(location_id):

    machines = db.session.query(Machine).filter(Machine.location_id == location_id).all()
    bulk_bookings = db.session.scalars(
        sqla.select(Booking).where(Booking.location_id == location_id)
    ).all()

    location = db.session.get(Location, location_id)
    if not location:
        flash("Location not found", "danger")
        return redirect(url_for('main.map_page'))

    return render_template(
        "index.html",   # reuse your existing machine page
        title=f"Location {location_id}",
        subtitle= location.name,
        machines=machines,
        bulk_bookings=bulk_bookings,
        location=location
    )

@bp_main.route('/location/<int:location_id>/review', methods=['GET', 'POST'])
@login_required
def location_review(location_id):
    location  = db.session.get(Location, location_id)
    if not location:
        flash("Location not found", "danger")
        return redirect(url_for('main.map_page'))
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            username=current_user.username,
            rating=form.rating.data,
            comment=form.comment.data,
            location = location
        )
        db.session.add(review)
        db.session.commit()
        flash("Review submitted successfully!", "success")
        return redirect(url_for('main.location', location_id=location_id))
    return render_template('create_Review.html', form=form, location=location)

@bp_main.route('/machine/<int:machine_id>/report', methods=['POST','GET'])
@login_required
def report(machine_id):
    
    machine = db.session.get(Machine, machine_id)
    if not machine:
        flash("Machine not found", "danger")
        return redirect(url_for('main.map_page'))
    
    rform = ReportForm()
    if rform.validate_on_submit():
        # Here you would typically save the report to the database
        report = Report(
            reason=rform.reason.data
        )
        report.machine = machine
        db.session.add(report)
        db.session.commit()
        flash(f"Report submitted for {machine.type} #{machine.id}", "success")
        return redirect(url_for('main.map_page'))
    return render_template('create_report.html', form=rform, machine=machine)

@bp_main.route('/machine/<int:machine_id>/disable', methods=['POST'])
@login_required
def disable_machine(machine_id):
    machine = db.session.get(Machine, machine_id)
    if not machine:
        flash("Machine not Found", "info")
        return redirect(url_for('main.map_page'))
    if current_user.user_type != "admin":
        flash("Unable to disable machine", "danger")
        return redirect(url_for('main.map_page'))
    
    machine.status = "broken"
    db.session.commit()
    flash(f"Machine {machine.type} #{machine.id} disabled", "success")
    return redirect(url_for('main.profile'))

@bp_main.route('/report/<int:report_id>/resolve', methods=['POST'])
@login_required
def report_resolve(report_id):
    
    report = db.session.get(Report, report_id)
    if not report:
        flash("Report not found", "danger")
        return redirect(url_for('main.profile'))
    
    machine = report.machine
    if machine:
        machine.status = "available"
        db.session.commit()

    db.session.delete(report)
    db.session.commit()
    flash("Report resolved", "success")
    return redirect(url_for('main.profile'))


@bp_main.route('/machine/<int:machine_id>/reserve_time', methods=['GET', 'POST'])
@login_required
def reserve_time(machine_id):
    """
    PURPOSE:
    - Displays available time slots for a machine.
    - Allows user to reserve a 1-hour block.
    """

    machine = db.session.get(Machine, machine_id)

    if not machine:
        flash("Machine not found.", "danger")
        return redirect(url_for('main.map_page'))

    # Generate time slots for today (8AM–8PM)
    today = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    start_hour = 8
    end_hour = 20

    time_slots = []

    for hour in range(start_hour, end_hour):
        start_time = today.replace(hour=hour)
        end_time = start_time + timedelta(hours=1)

        # Check if this time slot overlaps existing reservation
        existing = Reservation.query.filter(
            Reservation.machine_id == machine.id,
            Reservation.start_time < end_time,
            Reservation.end_time > start_time
        ).first()

        time_slots.append({
            "start": start_time,
            "end": end_time,
            "reserved": existing is not None
        })

    # If user submits reservation
    if request.method == 'POST':
        start_str = request.form.get("start_time")

        if start_str:
            start_time = datetime.fromisoformat(start_str)
            end_time = start_time + timedelta(hours=1)

            new_reservation = Reservation(
                machine_id=machine.id,
                user_id=current_user.id,
                start_time=start_time,
                end_time=end_time,
                location_id=machine.location_id
            )

            db.session.add(new_reservation)
            db.session.commit()

            flash("Reservation successful!", "success")
            return redirect(url_for('main.location', location_id=machine.location_id))

    return render_template(
        "reserve_time.html",
        machine=machine,
        time_slots=time_slots
    )



@bp_main.route('/machine/<int:machine_id>/calendar', methods=['GET', 'POST'])
@login_required
def machine_calendar(machine_id):

    machine = Machine.query.get_or_404(machine_id)

    if request.method == "POST":
        day = int(request.form["day"])
        hour = int(request.form["hour"])

        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

        # Find the Monday of THIS week
        start_of_week = today - timedelta(days=today.weekday())

        # Target date is fixed within this week
        target_date = start_of_week + timedelta(days=day)

        start_time = target_date.replace(hour=hour,
                                         minute=0,
                                         second=0,
                                         microsecond=0)
        end_time = start_time + timedelta(hours=1)

        existing = Reservation.query.filter_by(
            machine_id=machine_id,
            start_time=start_time
        ).first()

        if existing:
            flash("That time is already reserved.", "warning")

        else:
            new_res = Reservation(
                machine_id=machine_id,
                user_id=current_user.id,
                start_time=start_time,
                end_time=end_time
            )
            db.session.add(new_res)
            db.session.commit()

        return redirect(url_for('main.machine_calendar',
                                machine_id=machine_id))

    reservations = (
    Reservation.query
    .filter_by(machine_id=machine_id,
               user_id=current_user.id)   # only show YOUR reservations
    .order_by(Reservation.start_time)    # sort by day then time
    .all()
)

    calendar = {}
    for r in reservations:
        calendar[(r.start_time.weekday(), r.start_time.hour)] = r

    days = ["Monday","Tuesday","Wednesday","Thursday",
            "Friday","Saturday","Sunday"]

    return render_template(
        "machine_calendar.html",
        machine=machine,
        reservations=reservations,
        calendar=calendar,
        days=days
    )


@bp_main.route('/machine/<int:machine_id>/reserve', methods=['POST'])
@login_required
def reserve_slot(machine_id):
    machine = Machine.query.get_or_404(machine_id)
    data = request.get_json()
    day = int(data.get("day"))
    hour = int(data.get("hour"))

    # Calculate the next date for this weekday
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_weekday = today.weekday()  # 0=Monday ... 6=Sunday
    # adjust to match JS day (0=Sunday)
    day_offset = (day - ((today_weekday + 1) % 7)) % 7
    start_time = today + timedelta(days=day_offset, hours=hour)
    end_time = start_time + timedelta(hours=1)

    # Check if slot is already taken
    existing = Reservation.query.filter(
        Reservation.machine_id == machine.id,
        Reservation.start_time < end_time,
        Reservation.end_time > start_time
    ).first()

    if existing:
        return jsonify({"success": False, "message": "Slot already reserved."})

    # Create new reservation
    new_res = Reservation(
        machine_id=machine.id,
        user_id=current_user.id,
        start_time=start_time,
        end_time=end_time
    )
    db.session.add(new_res)
    db.session.commit()

    return jsonify({"success": True})


@bp_main.route('/location/<int:location_id>/location_data', methods=['GET'])
@login_required
def location_data(location_id):
    location = db.session.get(Location, location_id)
    if not location:
        return jsonify({"error": "Location not found"}), 404

    data = {
        'name': location.name,
        'num_machines': location.get_num_machines(),
        'num_available': location.get_num_available_machines()
    }

    return jsonify(data)


# TO MAKE MACHINES IN DB (run once) ----------------------------------
# For the 6 locations
# for location_id in range(1, 7):  # 6 locations
#     #Create 4 washers and 4 dryers for each location
#     for i in range(4):
#         washer = Machine(type="Washer", location_id=location_id)
#         dryer = Machine(type="Dryer", location_id=location_id)
#         db.session.add(washer)
#         db.session.add(dryer)
#         db.session.commit()


# # TO MAKE LOCATIONS IN DB (run once) ----------------------------------
# from app import db
# from app.main.models import Location

# names = ["West House", "Fruit House", "Oak House", "Cedar A", "Cedar B", "Sever House", "William House", "Marston A", "Marston B"]

# for name in names:
#     if not db.session.query(Location).filter_by(name=name).first():
#         db.session.add(Location(name=name))

# db.session.commit()
# print("Locations added (or already existed).")

@bp_main.route('/reservation/<int:reservation_id>/cancel',
               methods=['POST'])
@login_required
def cancel_calendar_reservation(reservation_id):

    reservation = db.session.get(Reservation, reservation_id)

    if reservation and reservation.user_id == current_user.id:
        machine_id = reservation.machine_id
        db.session.delete(reservation)
        db.session.commit()

        return redirect(url_for('main.machine_calendar',
                                machine_id=machine_id))

    return redirect(url_for('main.map_page'))



# THIS IS WHERE THE SECTIION STARTS FOR EDEN-BCG ROUTES -------------------------
# QUINTUPLETS

@bp_main.route('/admin')
@login_required
def admin_home():

    if current_user.user_type != "Admin":
        abort(403)

    return render_template("admin_home.html")

@bp_main.route('/driver')
@login_required
def driver_home():

    if current_user.user_type != "Driver":
        abort(403)

    return render_template("driver_home.html")


@bp_main.route('/driver/route/<int:route_number>')
@login_required
def driver_route(route_number):

    if current_user.user_type != "Driver":
        abort(403)

    if route_number not in range(1, 4):
        abort(404)

    return render_template(
        "driver_route_form.html",
        route_number=route_number
    )



# from app.main.forms import TruckLicensePlateForm
# from app.main.models import Truck

# @bp_main.route('/admin/sorting_form/truck_<int:truck_number>', methods=['GET', 'POST'])
# @login_required
# def driver_route(truck_number): # Note: Python doesn't allow duplicate function names, so make sure this is named distinctly if you have another 'driver_route' function!
#     if current_user.user_type != "Admin":
#         abort(403)
    
#     if truck_number not in range(1, 8):
#         abort(404)

#     # Find the truck or create it if it doesn't exist yet
#     truck = db.session.scalar(sqla.select(Truck).where(Truck.truck_number == truck_number))
    
#     form = TruckLicensePlateForm()
    
#     if form.validate_on_submit():
#         if not truck:
#             truck = Truck(truck_number=truck_number)
#             db.session.add(truck)
        
#         truck.license_plate = form.license_plate.data
#         db.session.commit()
        
#         flash(f"License plate for Truck #{truck_number} updated successfully!", "success")
#         return redirect(url_for('main.driver_route', truck_number=truck_number))
    
#     # Pre-populate the form if a license plate is already saved
#     if truck and not form.license_plate.data:
#         form.license_plate.data = truck.license_plate

#     return render_template(
#         "admin_sorting_center_form.html",
#         truck_number=truck_number,
#         form=form,
#         truck=truck
#     )


@bp_main.route('/daily-sorting-form')
@login_required
def daily_sorting_form():
    return render_template('admin_sorting_center_form.html', title='Daily Sorting Form')

