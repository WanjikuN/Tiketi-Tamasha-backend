from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from models import db, User, Role, Event, Payment, Category
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

fake = Faker()

def seed_users():
    with app.app_context():
        roles = Role.query.all()

        for _ in range(10):
            # Generate a random phone number and ensure it matches the expected format
            phone_number = None
            while not phone_number or not re.match(r'^\+?1?\d{9,15}$|\+?1?\d{3} ?\d{3} ?\d{3}$', phone_number):
                phone_number = fake.phone_number()

            user = User(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                phone_number=phone_number,
                role_id=fake.random_element(elements=roles).id
            )
            print("Adding user:", user)
            user.roles.append(fake.random_element(elements=roles))
            db.session.add(user)
            db.session.commit()  # Commit changes after seeding users
            print("Users added successfully.")

def seed_roles():
    with app.app_context():
        roles = ['Admin', 'Moderator', 'User']
        for role_name in roles:
            role = Role(name=role_name)
            db.session.add(role)
        db.session.commit()  # Commit changes after seeding roles
        print("Roles added successfully.")

def seed_events():
    with app.app_context():
        users = User.query.all()
        for _ in range(5):
            random_user = fake.random_element(elements=users)
            event = Event(
                event_name=fake.word(),
                description=fake.text(),
                location=fake.city(),
                start_time=fake.date_time_this_year(),
                end_time=fake.date_time_this_year(),
                early_booking_price=fake.random_int(min=50, max=100),
                MVP_price=fake.random_int(min=100, max=150),
                regular_price=fake.random_int(min=75, max=125),
                images=fake.image_url(),
                available_tickets=fake.random_int(min=50, max=200),
                category_id=fake.random_element(elements=(1, 2, 3))
            )
            # Associate the event with the random user
            event.users.append(random_user)

            db.session.add(event)
        db.session.commit()  # Commit changes after seeding events
        print("Events added successfully.")

def seed_payments():
    with app.app_context():
        for _ in range(10):
            payment = Payment(
                amount=fake.random_int(min=10, max=100), 
                payment_type=fake.random_element(elements=('Credit Card', 'Mpesa')),
                status=fake.random_element(elements=('Pending', 'Completed')),
                payment_date=fake.date_time_this_month(),
                user_id=fake.random_int(min=1, max=10),
                event_id=fake.random_int(min=1, max=5)
            )
            db.session.add(payment)
        db.session.commit()  # Commit changes after seeding payments
        print("Payments added successfully.")

def seed_categories():
    with app.app_context():
        categories = ['Music', 'Sports', 'Technology']
        for category_name in categories:
            category = Category(name=category_name)
            db.session.add(category)
        db.session.commit()  # Commit changes after seeding categories
        print("Categories added successfully.")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
        # Call seed functions
        seed_roles()
        seed_users()
        seed_categories()
        seed_events()
        seed_payments()

        db.session.commit()
