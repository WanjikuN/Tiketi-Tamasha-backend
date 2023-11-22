from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
# from falsk_cors import CORS
from models import db, Customer, EventOrganizer, Event, CustomerEvent
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
db.init_app(app)
api = Api(app)



class CustomerResource(Resource):
    def get(self, customer_id):
        customer = Customer.query.get(customer_id)
        if customer:
            return jsonify(customer.to_dict()), 200
        return make_response(jsonify({'message': 'Customer not found'}), 404)

    def post(self):
        data = request.get_json()
        try:
            new_customer = Customer(**data)
            db.session.add(new_customer)
            db.session.commit()
            return jsonify(new_customer.to_dict()), 201
        except ValueError as e:
            return make_response(jsonify({'error': str(e)}), 400)
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({'error': 'Duplicate entry'}), 400)

    def put(self, customer_id):
        data = request.get_json()
        customer = Customer.query.get(customer_id)
        if customer:
            try:
                for key, value in data.items():
                    setattr(customer, key, value)
                db.session.commit()
                return jsonify(customer.to_dict()), 200
            except ValueError as e:
                return make_response(jsonify({'error': str(e)}), 400)
        return make_response(jsonify({'message': 'Customer not found'}), 404)

    def delete(self, customer_id):
        customer = Customer.query.get(customer_id)
        if customer:
            db.session.delete(customer)
            db.session.commit()
            return make_response(jsonify({'message': 'Customer deleted'}), 200)
        return make_response(jsonify({'message': 'Customer not found'}), 404)

class EventOrganizerResource(Resource):
    def get(self, organizer_id):
        organizer = EventOrganizer.query.get(organizer_id)
        if organizer:
            return jsonify(organizer.to_dict()), 200
        return make_response(jsonify({'message': 'Event Organizer not found'}), 404)

    def post(self):
        data = request.get_json()
        try:
            new_organizer = EventOrganizer(**data)
            db.session.add(new_organizer)
            db.session.commit()
            return jsonify(new_organizer.to_dict()), 201
        except ValueError as e:
            return make_response(jsonify({'error': str(e)}), 400)
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({'error': 'Duplicate entry'}), 400)

    def put(self, organizer_id):
        data = request.get_json()
        organizer = EventOrganizer.query.get(organizer_id)
        if organizer:
            try:
                for key, value in data.items():
                    setattr(organizer, key, value)
                db.session.commit()
                return jsonify(organizer.to_dict()), 200
            except ValueError as e:
                return make_response(jsonify({'error': str(e)}), 400)
        return make_response(jsonify({'message': 'Event Organizer not found'}), 404)

    def delete(self, organizer_id):
        organizer = EventOrganizer.query.get(organizer_id)
        if organizer:
            db.session.delete(organizer)
            db.session.commit()
            return make_response(jsonify({'message': 'Event Organizer deleted'}), 200)
        return make_response(jsonify({'message': 'Event Organizer not found'}), 404)

class EventResource(Resource):
    def get(self, event_id):
        event = Event.query.get(event_id)
        if event:
            return jsonify(event.to_dict()), 200
        return make_response(jsonify({'message': 'Event not found'}), 404)

    def post(self):
        data = request.get_json()
        try:
            new_event = Event(**data)
            db.session.add(new_event)
            db.session.commit()
            return jsonify(new_event.to_dict()), 201
        except ValueError as e:
            return make_response(jsonify({'error': str(e)}), 400)
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({'error': 'Duplicate entry'}), 400)

    def put(self, event_id):
        data = request.get_json()
        event = Event.query.get(event_id)
        if event:
            try:
                for key, value in data.items():
                    setattr(event, key, value)
                db.session.commit()
                return jsonify(event.to_dict()), 200
            except ValueError as e:
                return make_response(jsonify({'error': str(e)}), 400)
        return make_response(jsonify({'message': 'Event not found'}), 404)

    def delete(self, event_id):
        event = Event.query.get(event_id)
        if event:
            db.session.delete(event)
            db.session.commit()
            return make_response(jsonify({'message': 'Event deleted'}), 200)
        return make_response(jsonify({'message': 'Event not found'}), 404)

class CustomerEventResource(Resource):
    def get(self, booking_id):
        booking = CustomerEvent.query.get(booking_id)
        if booking:
            return jsonify(booking.to_dict()), 200
        return make_response(jsonify({'message': 'Customer Event booking not found'}), 404)

    def post(self):
        data = request.get_json()
        try:
            new_booking = CustomerEvent(**data)
            db.session.add(new_booking)
            db.session.commit()
            return jsonify(new_booking.to_dict()), 201
        except ValueError as e:
            return make_response(jsonify({'error': str(e)}), 400)
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({'error': 'Duplicate entry'}), 400)

    def put(self, booking_id):
        data = request.get_json()
        booking = CustomerEvent.query.get(booking_id)
        if booking:
            try:
                for key, value in data.items():
                    setattr(booking, key, value)
                db.session.commit()
                return jsonify(booking.to_dict()), 200
            except ValueError as e:
                return make_response(jsonify({'error': str(e)}), 400)
        return make_response(jsonify({'message': 'Customer Event booking not found'}), 404)

    def delete(self, booking_id):
        booking = CustomerEvent.query.get(booking_id)
        if booking:
            db.session.delete(booking)
            db.session.commit()
            return make_response(jsonify({'message': 'Customer Event booking deleted'}), 200)
        return make_response(jsonify({'message': 'Customer Event booking not found'}), 404)



api.add_resource(CustomerResource, '/customer', '/customer/<int:customer_id>')
api.add_resource(EventOrganizerResource, '/event_organizer', '/event_organizer/<int:organizer_id>')
api.add_resource(EventResource, '/event', '/event/<int:event_id>')
api.add_resource(CustomerEventResource, '/customer_event', '/customer_event/<int:booking_id>')

if __name__== '__main__':
    app.run(debug=True, port=5000)