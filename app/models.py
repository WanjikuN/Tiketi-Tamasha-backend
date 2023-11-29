from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from flask_bcrypt import Bcrypt

import re

db = SQLAlchemy()
bcrypt=Bcrypt()

userRoles_association = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)
eventsUsers_association = db.Table(
    'event_users',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id')),
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'))
)


class Role(db.Model, SerializerMixin):
    __tablename__ = 'roles'

    serialize_rules = ('-users.roles',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    # Relationships
    users = db.relationship('User', secondary=userRoles_association, back_populates='roles')

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Role name cannot be empty.")
        return name


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-payments', '-roles', '-events')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    # relationships
    payments = db.relationship('Payment', backref='users')
    roles = db.relationship('Role', secondary=userRoles_association, back_populates='users')
    events = db.relationship('Event', secondary=eventsUsers_association, back_populates='users')

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

    @hybrid_property
    def password_hash(self):
        # return self._password_hash
        raise AttributeError('should not view password_hash')
    
    @password_hash.setter
    def password_hash(self, password):       
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))
        

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number:
            pattern = re.compile(r'^\+?1?\d{9,15}$|\+?1?\d{3} ?\d{3} ?\d{3}$')
            if not pattern.match(phone_number):
                raise ValueError("Invalid phone number format.")
        return phone_number


class Event(db.Model, SerializerMixin):
    __tablename__ = 'events'

    serialize_rules = ('-payments', '-categories', '-users')

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
    images = db.Column(db.String(255), nullable=True)
    available_tickets = db.Column(db.Integer, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    # relationships
    payments = db.relationship('Payment', backref='events')
    users = db.relationship('User', secondary=eventsUsers_association, back_populates='events')

    @validates('event_name')
    def validate_event_name(self, key, event_name):
        if not event_name:
            raise ValueError("Event name cannot be empty.")
        return event_name


class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'

    serialize_rules = ('-users', '-events')

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    payment_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

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


class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'

    serialize_rules = ('-events',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # relationships
    events = db.relationship('Event', backref='categories')

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Category name cannot be empty.")
        return name
