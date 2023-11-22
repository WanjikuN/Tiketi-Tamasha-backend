from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db, User, Role, Event, Payment, Category

def create_tables():
    engine = create_engine('sqlite:///test.db')
    db.metadata.create_all(engine)
    return engine

def test_user_model():
    engine = create_tables()
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        new_role = Role(name="Speaker")
        session.add(new_role)
        session.commit()
        print("Role added successfully.")

        new_customer = User(username="Joseph Parmuat", email="parmuatjoseph234@gmail.com", password="parmuat", phone_number="0706504461", role_id=new_role.id)
        session.add(new_customer)
        session.commit()
        print("Customer added successfully.")

        new_role_organizer = Role(name="Event sponsor")
        session.add(new_role_organizer)
        session.commit()
        print("Organizer Role added successfully.")

        new_organizer = User(username="Brian Almasi", email="brianalmasi84@gmail.com", password="almasi123", phone_number="0724486178", role_id=new_role_organizer.id)
        session.add(new_organizer)
        session.commit()
        print("Organizer added successfully.")

        event_date = datetime.strptime("2023-06-07", "%Y-%m-%d").date()

        new_category = Category(name="AI's")
        session.add(new_category)
        session.commit()
        print("Category added successfully.")

        new_event = Event(
            event_name="AI display",
            description="shaping developers",
            tags="speaker, sponsor",
            location="KICC",
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow(),
            early_booking_price=4000.0,
            MVP_price=6000.0,
            regular_price=6500.0,
            images="https://images.pexels.com/photos/16882422/pexels-photo-16882422/free-photo-of-close-up-of-a-group-of-people-holding-tickets.jpeg?auto=compress&cs=tinysrgb&w=600", 
            available_tickets=100,  
            user_id=new_customer.id,
            category_id=new_category.id
        )
        session.add(new_event)
        session.commit()
        print("Event added successfully.")

        new_payment = Payment(
            payment_type="Credit Card",
            status="Success",
            payment_date=datetime.utcnow(),
            amount=9800.0,
            user_id=new_customer.id,
            event_id=new_event.id
        )
        session.add(new_payment)
        session.commit()
        session.close()

        print("Payment added successfully.")

        all_events = session.query(Event).all()
        print("All Events:")
        for event in all_events:
            print(event.event_name, event.description, event.tags, event.location, event.start_time, event.end_time, event.early_booking_price, event.MVP_price, event.regular_price, event.user_id, event.category_id, event.images, event.available_tickets)

        all_payments = session.query(Payment).all()
        print("All Payments:")
        for payment in all_payments:
            print(payment.amount, payment.user_id, payment.event_id)

    except Exception as e:
        print("Error:", e)
        session.rollback()

if __name__ == "__main__":
    test_user_model()
