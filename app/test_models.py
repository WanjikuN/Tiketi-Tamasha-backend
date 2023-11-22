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

    new_role = Role(name="Customer")
    session.add(new_role)
    session.commit()

    new_customer = User(username="Maasai Obadia", email="obadiakim@gmail.com", password="obadia123", phone_number="0775649842", role_id=new_role.id)
    session.add(new_customer)
    session.commit()

    new_role_organizer = Role(name="Event Organizer")
    session.add(new_role_organizer)
    session.commit()

    new_organizer = User(username="Gideon Bett", email="bettgideon456@gmail.com", password="kiptoo", phone_number="0798667046", role_id=new_role_organizer.id)
    session.add(new_organizer)
    session.commit()

    event_date = datetime.strptime("2023-11-30", "%Y-%m-%d").date()

    new_category = Category(name="Tech")
    session.add(new_category)
    session.commit()

    new_event = Event(name="Droidcon", date=event_date, ticket_price=5000.0, category_id=new_category.id)
    session.add(new_event)
    session.commit()

    new_payment = Payment(amount=10000.0, user_id=new_customer.id, event_id=new_event.id)
    session.add(new_payment)
    session.commit()

    all_customers = session.query(User).filter_by(role_id=new_role.id).all()
    for customer in all_customers:
        print(customer.username, customer.email, customer.password, customer.phone_number)

    all_organizers = session.query(User).filter_by(role_id=new_role_organizer.id).all()
    for organizer in all_organizers:
        print(organizer.username, organizer.email, organizer.password, organizer.phone_number)

    all_events = session.query(Event).all()
    for event in all_events:
        print(event.name, event.date, event.ticket_price, event.category_id)

    all_payments = session.query(Payment).all()
    for payment in all_payments:
        print(payment.amount, payment.user_id, payment.event_id)

if __name__ == "__main__":
    test_user_model()
