from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Role name cannot be empty.")
        return name

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref('users', lazy=True))

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username cannot be empty.")
        return username

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise ValueError("Email cannot be empty.")
        if "@" not in email or "." not in email:
            raise ValueError("Invalid email address.")
        return email

    @validates('password')
    def validate_password(self, key, password):
        if not password:
            raise ValueError("Password cannot be empty.")
        return password

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number:
            pattern = re.compile(r'^\+?1?\d{9,15}$|\+?1?\d{3} ?\d{3} ?\d{3}$')
            if not pattern.match(phone_number):
                raise ValueError("Invalid phone number format.")
        return phone_number

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(200), nullable=True)
    location = db.Column(db.String(200), nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    early_booking_price = db.Column(db.Numeric(10, 2), nullable=True)
    MVP_price = db.Column(db.Numeric(10, 2), nullable=True)
    regular_price = db.Column(db.Numeric(10, 2), nullable=True)
    images = db.Column(db.String(255), nullable=True)  # Add 'images' column for storing image URLs
    available_tickets = db.Column(db.Integer, nullable=True)  # Add 'available_tickets' column for ticket count
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('events', lazy=True))

    @validates('event_name')
    def validate_event_name(self, key, event_name):
        if not event_name:
            raise ValueError("Event name cannot be empty.")
        return event_name


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('payments', lazy=True))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship('Event', backref=db.backref('payments', lazy=True))

    @validates('payment_type')
    def validate_payment_type(self, key, payment_type):
        if not payment_type:
            raise ValueError("Payment type cannot be empty.")
        return payment_type

    @validates('status')
    def validate_status(self, key, status):
        if not status:
            raise ValueError("Payment status cannot be empty.")
        return status
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Category name cannot be empty.")
        return name
