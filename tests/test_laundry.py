import os, sys

from config import TestConfig
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root)

from app import create_app, db


import pytest
from datetime import datetime,  timedelta

from app import db
from app.main.models import User, Booking, Machine, Admin,Location,Report,Reservation,Review


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def regular_user():
    u = User(
        username='testuser',
        email='testuser@example.com',
        address='123 Test St',
        user_type='User',
    )
    u.set_password('testpassword')
    db.session.add(u)
    db.session.commit()
    return u

@pytest.fixture
def driver_user():
    u = User(
        username='testuser2',
        email='testuser2@example.com',
        address='123 Test St',
        user_type='Driver',
    )
    u.set_password('testpassword')
    db.session.add(u)
    db.session.commit()
    return u

@pytest.fixture
def admin_user():
    a = Admin(
        username='testuser3',
        email='testuser3@example.com',
        user_type='Admin',
        location_id=1
    )
    a.set_password('testpassword')
    db.session.add(a)
    db.session.commit()
    return a

@pytest.fixture
def sample_data(regular_user):
    l = Location(name='testl')
    db.session.add(l)
    db.session.commit()

    m1 = Machine(type='washer', location_id=l.id)
    m2 = Machine(type='dryer', location_id=l.id)
    db.session.add(m1)
    db.session.add(m2)
    db.session.commit()

    b1 = Booking(user_id=regular_user.id, username=regular_user.username, email=regular_user.email, machine_type='washer', start_time=datetime.now() + timedelta(hours=1), end_time=datetime.now() + timedelta(hours=2))
    b2 = Booking(user_id=regular_user.id, username=regular_user.username, email=regular_user.email, machine_type='dryer', start_time=datetime.now() + timedelta(hours=2), end_time=datetime.now() + timedelta(hours=3))
    db.session.add(b1)
    db.session.add(b2)
    db.session.commit()

    res1 = Reservation(user_id=regular_user.id, machine_id=m1.id, start_time=datetime.now() + timedelta(hours=3), end_time=datetime.now() + timedelta(hours=4))
    res2 = Reservation(user_id=regular_user.id, machine_id=m2.id, start_time=datetime.now() + timedelta(hours=4), end_time=datetime.now() + timedelta(hours=5))
    db.session.add(res1)
    db.session.add(res2)
    db.session.commit()

    return {
        'location': l,
        'machines': [m1, m2],
        'bookings': [b1, b2],
        'reservations': [res1, res2],
    }

@pytest.fixture
def admin_data(admin_user):
    l = Location(name='testl')
    db.session.add(l)
    db.session.commit()

    m1 = Machine(type='washer', location_id=l.id)
    m2 = Machine(type='dryer', location_id=l.id)
    db.session.add(m1)
    db.session.add(m2)
    db.session.commit()

    rep = Report(machine_id=m1.id, reason='Machine not working')
    db.session.add(rep)
    db.session.commit()

    return {
        'location': l,
        'machines': [m1, m2],
        'report': rep
    }

@pytest.fixture
def driver_data(driver_user, regular_user):
    l = Location(name='testl')
    db.session.add(l)
    db.session.commit()

    m1 = Machine(type='washer', location_id=l.id)
    m2 = Machine(type='dryer', location_id=l.id)
    db.session.add(m1)
    db.session.add(m2)
    db.session.commit()

    
    b1 = Booking(user_id=regular_user.id, username=regular_user.username, email=regular_user.email, machine_type='washer', start_time=datetime.now() + timedelta(hours=1), end_time=datetime.now() + timedelta(hours=2))
    b2 = Booking(user_id=regular_user.id, username=regular_user.username, email=regular_user.email, machine_type='dryer', start_time=datetime.now() + timedelta(hours=2), end_time=datetime.now() + timedelta(hours=3))
    db.session.add(b1)
    db.session.add(b2)
    db.session.commit()

    return {
        'location': l,
        'machines': [m1, m2],
        'bookings': [b1, b2],
    }

def login(client, username, password):
    return client.post('/user/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def test_auth_registration(client):
    resp = client.get('/user/register')
    assert resp.status_code == 200

    resp = client.post('/user/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'address': '456 New St',
        'password': 'newpassword',
        'password2': 'newpassword',
        'user_type': 'User'
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert db.session.query(User).filter_by(username='newuser').one_or_none() is not None

def test_auth_admin_registration(client):
    resp = client.get('/user/admin_register')
    assert resp.status_code == 200

    resp = client.post('/user/admin_register', data={
        'username': 'newadmin',
        'email': 'newadmin@example.com',
        'password': 'newpassword',
        'password2': 'newpassword',
        'location': '1'
    }, follow_redirects=True)

    assert resp.status_code == 200

    admin = db.session.query(User).filter_by(username='newadmin').one_or_none()
    assert admin is not None
    assert admin.user_type == 'Admin'
    assert db.session.query(Admin).where(Admin.id == admin.id, Admin.location_id == 1).one_or_none() is not None


def test_auth_login(client, regular_user):
    resp = client.get('/user/login')
    assert resp.status_code == 200

    resp = client.post('/user/login', data={
        'username': regular_user.username,
        'password': 'testpassword'
    }, follow_redirects=True)
    assert resp.status_code == 200

def test_auth_logout(client, regular_user):
    login(client, regular_user.username, 'testpassword')
    resp = client.get('/user/logout', follow_redirects=True)
    assert resp.status_code == 200

def test_main_profile_user(client, regular_user):
    login(client, regular_user.username, 'testpassword')
    resp = client.get('/profile')
    assert resp.status_code == 200
    assert b"Your Reservations" in resp.data

def test_main_profile_driver(client, driver_user, driver_data):
    login(client, driver_user.username, 'testpassword')
    resp = client.get('/profile')
    assert resp.status_code == 200
    assert b"Your Deliveries" in resp.data

def test_main_profile_admin(client, admin_user, admin_data):
    login(client, admin_user.username, 'testpassword')
    resp = client.get('/profile')
    assert resp.status_code == 200
    assert b"Your Reports" in resp.data

def test_main_reserve_bulk(client, regular_user, sample_data):
    login(client, regular_user.username, 'testpassword')
    resp = client.post(f'/reserve_bulk', data={
        'username': regular_user.username,
        'address': regular_user.address,
        'machine_type': 'washer',
        'start_time': (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M'),
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert db.session.query(Reservation).filter_by(user_id=regular_user.id).count() > 0

def test_main_cancel_reservation(client, regular_user, sample_data):
    login(client, regular_user.username, 'testpassword')
    machine = sample_data['machines'][0]
    resp = client.post(f'/machine/{machine.id}/cancel', follow_redirects=True)
    assert resp.status_code == 200
    assert db.session.query(Reservation).filter_by(id=machine.reserved_by == regular_user).one_or_none() is None

def test_main_map_page(client, regular_user):
    login(client, regular_user.username, 'testpassword')
    resp = client.get('/map')
    assert resp.status_code == 200

def test_main_location(client, regular_user, sample_data):
    login(client, regular_user.username, 'testpassword')
    location_id = sample_data['location'].id
    resp = client.get(f'/location/{location_id}')
    print(resp.location)
    assert resp.status_code == 200

def test_main_location_review(client, regular_user, sample_data):
    login(client, regular_user.username, 'testpassword')
    location_id = sample_data['location'].id
    resp = client.post(f'/location/{location_id}/review', data={
        'rating': '5',
        'comment': 'Great location!'
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert db.session.query(Review).filter_by(username=regular_user.username, location_id=location_id).one_or_none() is not None

def test_main_machine_report(client, regular_user, sample_data):
    login(client, regular_user.username, 'testpassword')
    machine_id = sample_data['machines'][0].id
    resp = client.post(f'/machine/{machine_id}/report', data={
        'reason': 'Washer is broken'
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert db.session.query(Report).filter_by(reason='Washer is broken', machine_id=sample_data['machines'][0].id).one_or_none() is not None

def test_main_machine_disable(client, admin_user, sample_data):
    login(client, admin_user.username, 'testpassword')
    machine_id = sample_data['machines'][0].id
    resp = client.post(f'/machine/{machine_id}/disable', follow_redirects=True)
    assert resp.status_code == 200
    machine = db.session.query(Machine).filter_by(id=machine_id).one()
    assert machine.status == 'broken'

def test_main_report_resolve(client, admin_user, admin_data):
    login(client, admin_user.username, 'testpassword')
    report_id = admin_data['report'].id
    resp = client.post(f'/report/{report_id}/resolve', follow_redirects=True)
    assert resp.status_code == 200
    report = db.session.query(Report).filter_by(id=report_id).one_or_none()
    assert report is None

def test_main_machine_reserve_time(client, regular_user, sample_data):
    login(client, regular_user.username, 'testpassword')
    machine_id = sample_data['machines'][0].id

    resp = client.get(f'/machine/{machine_id}/reserve_time')
    assert resp.status_code == 200

    # Page should contain at least one time slot (8AM–8PM)
    assert b"Reserve a Time Slot" in resp.data or b"start_time" in resp.data



def test_main_machine_calendar(client, regular_user, sample_data):
    login(client, regular_user.username, 'testpassword')
    machine_id = sample_data['machines'][0].id
    resp = client.get(f'/machine/{machine_id}/calendar')
    assert resp.status_code == 200

def test_main_machine_reserve(client, regular_user, sample_data):
    login(client, regular_user.username, "testpassword")
    machine_id = sample_data["machines"][0].id
    resp = client.post(
        f"/machine/{machine_id}/reserve",
        json={"day": 0, "hour": 10},
    )
    assert resp.status_code == 200
    assert resp.json["success"] is True
    reservation = Reservation.query.filter_by(
        machine_id=machine_id,
        user_id=regular_user.id
    ).first()
    assert reservation is not None

def test_main_machine_location_data(client, regular_user, sample_data):
    login(client, regular_user.username, 'testpassword')
    location_id = sample_data['location'].id
    resp = client.get(f'/location/{location_id}/location_data')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['num_machines'] == 2
    assert data['num_available'] == 2