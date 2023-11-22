from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db, Customer, EventOrganizer, Event, CustomerEvent

def create_tables():
    engine = create_engine('sqlite:///test.db')
    db.metadata.create_all(engine)
    return engine

def test_customer_model():
    engine = create_tables()
    Session = sessionmaker(bind=engine)
    session = Session()

    new_customer = Customer(name="Maasai Obadia", email="obadiakim@gmail.com", password="obadia123", phone_number="0775649842")
    session.add(new_customer)
    session.commit()

    new_organizer = EventOrganizer(name="Gideon Bett", email="bettgideon456@gmail.com", password="kiptoo", phone_number="0798667046")
    session.add(new_organizer)
    session.commit()

    event_date = datetime.strptime("2023-11-30", "%Y-%m-%d").date()

    new_event = Event(name="Droidcon", date=event_date, ticket_price=5000.0, organizer_id=new_organizer.id)
    session.add(new_event)
    session.commit()

    new_customer_event = CustomerEvent(customer_id=new_customer.id, event_id=new_event.id, tickets_purchased=2)
    session.add(new_customer_event)
    session.commit()

    all_customers = session.query(Customer).all()
    for customer in all_customers:
        print(customer.name, customer.email, customer.password, customer.phone_number)

    all_organizers = session.query(EventOrganizer).all()
    for organizer in all_organizers:
        print(organizer.name, organizer.email, organizer.password, organizer.phone_number)

    all_events = session.query(Event).all()
    for event in all_events:
        print(event.name, event.date, event.ticket_price, event.organizer_id)

    all_customer_events = session.query(CustomerEvent).all()
    for customer_event in all_customer_events:
        print(customer_event.customer_id, customer_event.event_id, customer_event.tickets_purchased)

if __name__ == "__main__":
    test_customer_model()
