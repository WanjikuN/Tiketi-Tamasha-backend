from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name cannot be empty.")
        return name

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

class EventOrganizer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name cannot be empty.")
        return name

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
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    ticket_price = db.Column(db.Numeric(10, 2), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('event_organizer.id'), nullable=False)
    organizer = db.relationship('EventOrganizer', backref=db.backref('events', lazy=True))

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Event name cannot be empty.")
        return name

class CustomerEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    tickets_purchased = db.Column(db.Integer, nullable=False, default=0)

    customer = db.relationship('Customer', backref=db.backref('booked_events', lazy=True))
    event = db.relationship('Event', backref=db.backref('attendees', lazy=True))
