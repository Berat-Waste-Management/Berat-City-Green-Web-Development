from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import WriteOnlyMapped
from sqlalchemy import event, JSON
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

from app import db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

class User(UserMixin,db.Model):
    __tablename__='user'
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    username: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64))
    email: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120))
    user_type: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))
    address: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(256), nullable=True)
    password_hash: sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(256))

    create_bookings: sqlo.Mapped[List["Booking"]] = sqlo.relationship("Booking",foreign_keys="Booking.user_id",back_populates= "user")
    claim_bookings: sqlo.Mapped[List["Booking"]] = sqlo.relationship("Booking", foreign_keys="Booking.driver_id", back_populates= "driver")

    reservations: sqlo.Mapped[List["Reservation"]] = sqlo.relationship("Reservation", back_populates="user", foreign_keys="[Reservation.user_id]")
    #reserved_machines: sqlo.Mapped[List["Reservation"]] = sqlo.relationship("Reservation", back_populates="reserved_by",foreign_keys="[Reservation.reserved_by_id]")

    __mapper_args__ = {
        'polymorphic_identity' : 'User',
        'polymorphic_on' : user_type
    }


    def __repr__(self):
        return f"<User ={self.username}>"
    
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    def get_user_bookings(self):
        return self.create_bookings

# ----------------------------------------------------------------------

# OLD ADMIN CLASS FROM LAUNDRY APP HERE TO REFERENCE IF ANYTHING GOES WRONG
# class Admin(User):
#     __tablename__='admin'

#     id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, sqla.ForeignKey('user.id'), primary_key=True)
#     location_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, sqla.ForeignKey('location.id'))

#     __mapper_args__ = {
#         'polymorphic_identity' : 'Admin'
#     }


#     def __repr__(self):
#         return f"<User ={self.username}>"
    
#     def set_password(self, password: str):
#         self.password_hash = generate_password_hash(password)
#     def check_password(self, password: str) -> bool:
#         return check_password_hash(self.password_hash, password)

class Admin(User):
    __tablename__ = 'admin'

    id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, sqla.ForeignKey('user.id'), primary_key=True)

    location_id: sqlo.Mapped[Optional[int]] = sqlo.mapped_column(sqla.Integer, sqla.ForeignKey('location.id'), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'Admin'
    }

    def __repr__(self):
        return f"<Admin ={self.username}>"

# OLD CLASS
# class Driver(User):
#     __tablename__='driver'

#     __mapper_args__ = {
#         'polymorphic_identity' : 'Driver'
#     }
#     id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, sqla.ForeignKey('user.id'), primary_key=True)

#     def __repr__(self):
#         return f"<User ={self.username}>"
    
#     def set_password(self, password: str):
#         self.password_hash = generate_password_hash(password)
#     def check_password(self, password: str) -> bool:
#         return check_password_hash(self.password_hash, password)
    
# ----------------------------------------------------------------------

class Driver(User):
    __tablename__ = 'driver'

    id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, sqla.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'Driver'
    }

    def __repr__(self):
        return f"<Driver ={self.username}>"

class Booking(db.Model):
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    user_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey("user.id"))
    driver_id: sqlo.Mapped[Optional[int]] = sqlo.mapped_column(sqla.ForeignKey("user.id"),nullable=True)
    address: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(200))
    location: sqlo.Mapped[Optional["Location"]] = sqlo.relationship("Location", back_populates="bookings")
    location_id: sqlo.Mapped[Optional[int]] = sqlo.mapped_column(sqla.Integer, sqla.ForeignKey('location.id'))
    user: sqlo.Mapped["User"] = sqlo.relationship("User", foreign_keys=[user_id], back_populates="create_bookings")
    driver: sqlo.Mapped["Driver"] = sqlo.relationship("Driver", foreign_keys=[driver_id], back_populates="claim_bookings")
    status: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50), default="Pending")
    progress: sqlo.Mapped[List[str]] = sqlo.mapped_column(JSON, default=lambda:["Pending"])
    machine_type: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))
    start_time: sqlo.Mapped[Optional[datetime]] = sqlo.mapped_column(default = lambda : datetime.now(timezone.utc))

    
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Machine(db.Model):
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    type: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(10))
    is_reserved: sqlo.Mapped[bool] = sqlo.mapped_column(sqla.Boolean, default=False)
    reserved_by_id: sqlo.Mapped[Optional[int]] = sqlo.mapped_column(sqla.Integer, sqla.ForeignKey('user.id'))
    reserved_by: sqlo.Mapped[Optional["User"]] = sqlo.relationship("User")
    reserved_until: sqlo.Mapped[Optional[datetime]] = sqlo.mapped_column(sqla.DateTime(timezone=True), nullable=True)
    reserved_time: sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(20))
    location_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, sqla.ForeignKey('location.id'), nullable=False)
    location: sqlo.Mapped[Optional["Location"]] = sqlo.relationship("Location", back_populates="machines")
    reports: sqlo.Mapped[List["Report"]] = sqlo.relationship("Report", back_populates="machine")
    status: sqlo.Mapped[str] = sqlo.mapped_column(sqla.Enum("available", "in-use", "broken", name="machine_status"), default="available")
    
    def reserved(self):
        return self.is_reserved and self.reserved_until > datetime.now(timezone.utc)
    
    def get_location(self):
        return self.location.name
            
class Location(db.Model):
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    name: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))
    machines: sqlo.Mapped[List["Machine"]] = sqlo.relationship("Machine", back_populates="location")

    reviews: sqlo.Mapped[List["Review"]] = sqlo.relationship("Review", back_populates="location")
    reservations: sqlo.Mapped[List["Reservation"]] = sqlo.relationship("Reservation", back_populates="location")
    bookings: sqlo.Mapped[List["Booking"]] = sqlo.relationship("Booking", back_populates="location")

    def get_name(self):
        return self.name
    
    def get_num_available_machines(self):
        count = 0
        for machine in self.machines:
            if not machine.reserved():
                count += 1
        return count
    
    def get_num_machines(self):
        return len(self.machines)

class Report(db.Model):
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    machine_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, sqla.ForeignKey('machine.id'))
    machine: sqlo.Mapped["Machine"] = sqlo.relationship("Machine", back_populates="reports")
    reason: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(500))

class Review(db.Model):
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    username: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64))
    rating: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer)
    comment: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(500))
    location_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, sqla.ForeignKey('location.id'))
    location: sqlo.Mapped["Location"] = sqlo.relationship("Location", back_populates="reviews")

class Reservation(db.Model):
    __tablename__ = "reservation"

    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    machine_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, sqla.ForeignKey('machine.id'), nullable=False)
    machine = db.relationship("Machine", backref="reservations")

    user_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, sqla.ForeignKey('user.id'), nullable=False)
    user: sqlo.Mapped["User"] = sqlo.relationship("User", back_populates="reservations", foreign_keys=[user_id])

    start_time: sqlo.Mapped[datetime] = sqlo.mapped_column(sqla.DateTime, nullable=False)
    end_time: sqlo.Mapped[datetime] = sqlo.mapped_column(sqla.DateTime, nullable=False)

    location_id: sqlo.Mapped[Optional[int]] = sqlo.mapped_column(sqla.Integer, sqla.ForeignKey('location.id'), nullable=True)
    location: sqlo.Mapped[Optional["Location"]] = sqlo.relationship("Location", back_populates="reservations")

    def __repr__(self):
        return f"{self.get_machine_location()}: {self.machine.type} #{self.machine_id} from {self.start_time} to {self.end_time}"
    def get_machine_location(self):
        return self.machine.get_location()
