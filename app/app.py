# from flask import Flask
from flask_migrate import Migrate
from flask import Flask, jsonify, request, make_response, session
from flask_restx import Api,Resource,reqparse,fields
from werkzeug.exceptions import NotFound
from werkzeug.security import generate_password_hash
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from models import db, Event, Payment, Role, Category, User, eventsUsers_association
import os
from dotenv import load_dotenv
load_dotenv()
# from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import random
import string
# Daraja
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.secret_key ="12jdhRIF567@#dzv&zhW"
# migrate = Migrate(app.db)
db.init_app(app)
migrate = Migrate(app, db)

api = Api(app , title='Ticketi Tamasha API ', version='0.0.1', description=' Ticketing site API Documentation', default='All')
CORS(app, supports_credentials=True)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)



base_url = 'https://tiketi-tamasha-backend.onrender.com'
consumer_keys = 'TKbOPVqsnYJpiDvQNlcQlMQP5P1Ch2c0'
consumer_secrets = 'YG2R7UVJfKtj8MkK'

# Create namespaces
stk_ns = api.namespace('STK-Push', description='MPESA STK operations')
login_ns = api.namespace('Login', description='User Login operations')
signup_ns = api.namespace('Signup', description='User Signup operations')
users_ns = api.namespace('Users', description='User operations')
events_ns = api.namespace('Events', description='Event operations')
payments_ns = api.namespace('Payments', description='Payment operations')
roles_ns = api.namespace('Roles', description='Role operations')
categories_ns = api.namespace('Categories', description='Category operations')

@stk_ns.route('/')
class Stk_Push(Resource):
    @staticmethod
    def _access_token():
        consumer_key = consumer_keys
        consumer_secret = consumer_secrets
        endpoint = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

        r = requests.get(endpoint, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        data = r.json()
        return data['access_token']
        
    @api.doc(params={'amount': 'The amount for the STK push', 'phone': 'The phone number for the STK push 254'})
    @cross_origin(supports_credentials=True)
    def get(self):
        amount = request.args.get('amount')
        phone = request.args.get('phone')

        endpoint = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

        access_token = Stk_Push._access_token()
        headers = {"Authorization": "Bearer %s" % access_token}
        my_endpoint = base_url + "/lnmo"
        Timestamp = datetime.now()
        times = Timestamp.strftime("%Y%m%d%H%M%S")
        password = "174379" + "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919" + times
        datapass = base64.b64encode(password.encode('utf-8')).decode("utf-8")

        data = {
            "BusinessShortCode": "174379",
            "Password": datapass,
            "Timestamp": times,
            "TransactionType": "CustomerPayBillOnline",
            "PartyA": phone,
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": my_endpoint,
            "AccountReference": "Tiketi Tamasha",
            "TransactionDesc": "HelloTest",
            "Amount": amount
        }

        res = requests.post(endpoint, json=data, headers=headers)
        parser = reqparse.RequestParser()
        parser.add_argument('amount', type=float, help='Amount to be processed', required=True)
        parser.add_argument('phone', type=str, help='Phone number to process', required=True)
        args = parser.parse_args()
        return res.json()
    
    @cross_origin(supports_credentials=True)
    def post(self):
        data = request.get_json()
        print(data)

        items = data.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata', {}).get('Item', [])
        print(items)
        for item in items:
            name = item.get('Name')
            value = item.get('Value')
            print(f"{name}, {value}")

        with open('lnmo.json', 'w') as f:
            f.write(json.dumps(data))
        return jsonify({"status": "success"})


api.add_resource(Stk_Push, '/lnmo', endpoint='lnmo')

@signup_ns.route('/')
class SignUp(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, help='Username',location='json', required=True)
    parser.add_argument('_password_hash', type=str, help='Hashed Password',location='json', required=True)
    parser.add_argument('email', type=str, help='Email',location='json', required=True)
    parser.add_argument('phone_number', type=str, help='Phone Number',location='json', required=True)
    parser.add_argument('role_id', type=int, help='Role ID',location='json', required=True)

    @api.expect(parser)
    def post(self):
        data = request.get_json()

        # name = data.get('name')
        username = data.get('username')
        password = data.get('_password_hash')  
        email = data.get('email')
        phone_number = data.get('phone_number')
        role_id = data.get('role_id')

        if not username or not password or role_id is None:
            return {'message': 'Username, password, and role_id are required'}, 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {'message': 'Username already in use. Please choose a different one.'}, 400
        
        newuser = User(username=username, _password_hash=generate_password_hash(password), email=email, phone_number=phone_number, role_id=role_id)

        db.session.add(newuser)
        db.session.commit()

        session['userid'] = newuser.id
        response = make_response("Login successful")
        response.set_cookie("userid", str(newuser.id))
        return make_response(newuser.to_dict(), 201)


api.add_resource(SignUp, '/signup', endpoint='signup')

@login_ns.route('/')
class LoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, help='Email', location='json', required=True)
    parser.add_argument('_password_hash', type=str, help='Password', location='json', required=True)

    @api.expect(parser)
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('_password_hash')

        if email and password:
            user = User.query.filter(User.email == email).first()
            if user and user.authenticate(password):
                session["user_id"] = user.id 
                return make_response(user.to_dict(), 200)

        return jsonify({"error": "Email or password is incorrect"}), 401


api.add_resource(LoginResource, '/login', endpoint='login')
class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['userid'] = None
            return jsonify({'message': 'User logged out successfully'})
        else:
            return {"error": "User must be logged in"}


api.add_resource(Logout, '/logout', endpoint='logout')


@events_ns.route('/','/<int:event_id>')
class Eventors(Resource):
    def get(self, event_id=None):
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        offset = (page - 1) * limit
        user_id = request.args.get('user_id') 
        print(f"Received request for event ID: {event_id}")

        if user_id:
        # Filter events based on the user_id
            events = Event.query.join(eventsUsers_association).filter_by(users_id=user_id).all()
            event_list = [{"event_id": event.id, **event.to_dict()} for event in events]
            response = make_response(jsonify(event_list), 200)
        elif event_id is None:
            # If user_id is not provided and event_id is None, return all events
            event_list = [{"event_id": n.id, **n.to_dict()} for n in Event.query.all()]
            response = make_response(jsonify(event_list), 200)
        else:
            # If event_id is provided, return the specific event
            event = Event.query.get(event_id)
            if event:
                response = make_response({"event_id": event.id, **event.to_dict()}, 200)
            else:
                response = make_response({"message": "Event not found"}, 404)

        return response
    parser = reqparse.RequestParser()
    parser.add_argument('event_name', type=str, help='Event Name',location='json', required=True)
    parser.add_argument('start_time', type=str, help='Start Time',location='json', required=True)
    parser.add_argument('end_time', type=str, help='End Time',location='json', required=True)
    parser.add_argument('location', type=str, help='Event Location',location='json', required=True)
    parser.add_argument('description', type=str, help='Event Description',location='json', required=True)
    parser.add_argument('MVP_price', type=float, help='MVP Price',location='json', required=True)
    parser.add_argument('regular_price', type=float, help='Regular Price',location='json', required=True)
    parser.add_argument('early_booking_price', type=float, help='Early Booking Price',location='json', required=True)

    @api.expect(parser)
    def post(self):
        data = request.get_json() 
        user_id = data['user_id'] 
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404     
        
        newrec = Event(
            event_name=data.get('event_name'),
            start_time=datetime.strptime(data.get('start_time'), "%Y-%m-%d %H:%M:%S.%f"),
            end_time=datetime.strptime(data.get('end_time'), "%Y-%m-%d %H:%M:%S.%f"),
            location=data.get('location'),
            description=data.get('description'),
            MVP_price=data.get('MVP_price'),
            regular_price=data.get('regular_price'),
            early_booking_price=data.get('early_booking_price'),
            tags=','.join(data.get('tags')),
            images=data.get('images'),
            available_tickets=data.get('available_tickets'),
            category_id=data.get('category_id'),
        )
        db.session.add(newrec)
        db.session.commit()
        newrec.users.append(user)
        
        db.session.commit()

        newrec_dict = newrec.to_dict()

        response = make_response(jsonify(newrec_dict))
        response.content_type = 'application/json'

        return response

        
    def delete(self, event_id):
        
        event = Event.query.get(event_id)
        if event:
            db.session.delete(event)
            db.session.commit()
            return {'message': 'Event deleted successfully'}, 200
        else:
            return {'message': 'Event not found'}, 404
    update_event_model = api.model('UpdateEvent', {
            'event_name': fields.String( description='Event Name'),
            'start_time': fields.String( description='Start Time'),
            'end_time': fields.String( description='End Time'),
            'location': fields.String( description='Event Location'),
            'description': fields.String( description='Event Description'),
            'MVP_price': fields.Float( description='MVP Price'),
            'regular_price': fields.Float( description='Regular Price'),
            'early_booking_price': fields.Float( description='Early Booking Price'),
                }) 
    @api.expect(update_event_model)   
    def patch(self, event_id):
        
        event = Event.query.get(event_id)
        if event:
            data = request.get_json()
            event.event_name = data.get('event_name', event.event_name)
            event.location = data.get('location', event.location)
            event.description = data.get('description', event.description)
           
            db.session.commit()
            updated_event_data = {
                'event_id': event.id,
                'event_name': event.event_name,
                'location': event.location,
                'description': event.description,
                
            }
            return {'message': 'Event updated successfully','updated_event': updated_event_data}, 200
        else:
            return {'message': 'Event not found'}, 404    
  
        
    
api.add_resource(Eventors, '/events', '/events/<int:event_id>', endpoint='events')


@payments_ns.route('/', '/<int:payment_id>')
class PaymentResource(Resource):
    def get(self):
        # Get the logged-in user's ID from the session
        user_id = session.get('user_id')

        if user_id:
            payments = Payment.query.filter_by(user_id=user_id).all()
        else:
            payments = Payment.query.all()

        payment_list = []

        for payment in payments:
            payment_dict = payment.to_dict()

            event = Event.query.get(payment.event_id)
            if event:
                payment_dict['event_name'] = event.event_name

            user = User.query.get(payment.user_id)
            if user:
                payment_dict['payer_phone'] = user.phone_number

            payment_list.append(payment_dict)
            return make_response(jsonify(payment_list), 200)
        else:
            return {'message': 'User not logged in'}, 401

    parser = reqparse.RequestParser()
    parser.add_argument('payment_type', type=str, help='Type of payment',location='json', required=True)
    parser.add_argument('payment_date', type=str, help='Date of payment',location='json', required=True)
    parser.add_argument('user_id', type=int, help='User ID',location='json', required=True)
    parser.add_argument('status', type=str, help='Payment status',location='json', required=True)
    parser.add_argument('event_id', type=int, help='Event ID',location='json', required=True)

    @api.expect(parser)
    def post(self):
        data = request.get_json()
        print("Received POST request:", data)
        new_payment = Payment(
            payment_type=data.get('payment_type'),
            payment_date=data.get('payment_date'),
            user_id=data.get('user_id'),
            status=data.get('status'),
            event_id=data.get('event_id'),
        )
        db.session.add(new_payment)
        db.session.commit()

        new_payment_dict = new_payment.to_dict()

        return make_response(jsonify(new_payment_dict), 201)
    def delete(self, payment_id):
        payment = Payment.query.get(payment_id)
        if payment:
            db.session.delete(payment)
            db.session.commit()
            return {'message': 'Payment deleted successfully'}, 200
        else:
            return {'message': 'Payment not found'}, 404
    update_payment_model = api.model('UpdatePayment', {
    'payment_type': fields.String(description='Updated payment type'),
    'payment_date': fields.String(description='Updated payment date'),
    'user_id': fields.Integer(description='Updated user ID'),
    'status': fields.String(description='Updated payment status'),
    'event_id': fields.Integer(description='Updated event ID'),
   
    })
    @api.expect(update_payment_model)
    def put(self, payment_id):
        payment = Payment.query.get(payment_id)
        if payment:
            data = request.get_json()
            payment.payment_type = data.get('payment_type', payment.payment_type)
            payment.payment_date = data.get('payment_date', payment.payment_date)
            
            db.session.commit()
            return {'message': 'Payment updated successfully'}, 200
        else:
            return {'message': 'Payment not found'}, 404    

        
api.add_resource(PaymentResource, '/payments', '/payments/<int:payment_id>', endpoint='payments')


@roles_ns.route('/', '/<int:role_id>')
class RoleResource(Resource):
    def get(self):
        roles = Role.query.all()
        role_dict = [role.to_dict() for role in roles]
        return make_response(jsonify(role_dict), 200)
    
    parser = reqparse.RequestParser()
    parser.add_argument('role_name', type=str, help='Role Name',location='json', required=True)
    parser.add_argument('description', type=str, help='Role Description',location='json', required=True)

    @api.expect(parser)
    def post(self):
        data = request.get_json()
        
        new_role = Role(
            role_name=data.get('role_name'),
            description=data.get('description'),
            
        )
        db.session.add(new_role)
        db.session.commit()
        new_role_dict = new_role.to_dict()
        return make_response(jsonify(new_role_dict), 201)
    
    def delete(self, role_id):
        role = Role.query.get(role_id)
        if role:
            db.session.delete(role)
            db.session.commit()
            return {'message': 'Role deleted successfully'}, 200
        else:
            return {'message': 'Role not found'}, 404
    update_role_model = api.model('UpdateRole', {
    'role_name': fields.String(description='Updated role name'),
    'description': fields.String(description='Updated role description'),
    
    })
    @api.expect(update_role_model)
    def put(self, role_id):
        role = Role.query.get(role_id)
        if role:
            data = request.get_json()
            role.name = data.get('name', role.name)
           
            db.session.commit()
            return {'message': 'Role updated successfully'}, 200
        else:
            return {'message': 'Role not found'}, 404
        
api.add_resource(RoleResource, '/roles','/roles/<int:role_id>', endpoint='roles')

@categories_ns.route('/', '/<int:category_id>')
class CategoryResource(Resource):
    def get(self):
        categories = Category.query.all()
        category_dict = [category.to_dict() for category in categories]
        return make_response(jsonify(category_dict), 200)
    
    parser = reqparse.RequestParser()
    parser.add_argument('category_name', type=str, help='Category Name',location='json', required=True)
    parser.add_argument('event_id', type=int, help='Event ID',location='json', required=True)

    @api.expect(parser)
    def post(self):
        data = request.get_json()
        
        new_category = Category(
            name=data.get('name'),
                   
        )
        db.session.add(new_category)
        db.session.commit()  

        new_category_dict = new_category.to_dict()
        return make_response(jsonify(new_category_dict), 201)
        
    def delete(self, category_id):
        category = Category.query.get(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
            return {'message': 'Category deleted successfully'}, 200
        else:
            return {'message': 'Category not found'}, 404
    update_category_model = api.model('UpdateCategory', {
    'category_name': fields.String(description='Updated category name'),
    'event_id': fields.Integer(description='Updated event ID'),
    
    })
    @api.expect(update_category_model)
    def put(self, category_id):
        category = Category.query.get(category_id)
        if category:
            data = request.get_json()
            category.name = data.get('name', category.name)
            
            db.session.commit()
            return {'message': 'Category updated successfully'}, 200
        else:
            return {'message': 'Category not found'}, 404
api.add_resource(CategoryResource, '/categories','/categories/<int:category_id>', endpoint='categories')
@users_ns.route('/', '/<int:user_id>')
class UserResource(Resource):
    def get(self, user_id=None):
        if user_id is not None:
            user = User.query.get(user_id)
            if user:
                user_dict = user.to_dict()
                return make_response(jsonify(user_dict), 200)
            else:
                return {'message': 'User not found'}, 404
        else:
            users = User.query.all()
            user_list = [user.to_dict() for user in users]
            return make_response(jsonify(user_list), 200)

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, help='Username', location='json', required=True)
    parser.add_argument('email', type=str, help='Email', location='json', required=True)
    parser.add_argument('phone_number', type=str, help='Phone Number', location='json', required=True)
    parser.add_argument('role_id', type=int, help='Role ID', location='json', required=True)

    @api.expect(parser)
    def post(self):
        data = request.get_json()

        username = data.get('username')
        email = data.get('email')
        phone_number = data.get('phone_number')
        role_id = data.get('role_id')

        if not username or not email or not phone_number or role_id is None:
            return {'message': 'Username, email, phone_number, and role_id are required'}, 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {'message': 'Username already in use. Please choose a different one.'}, 400

        new_user = User(
            username=username,
            email=email,
            phone_number=phone_number,
            role_id=role_id
        )

        db.session.add(new_user)
        db.session.commit()

        new_user_dict = new_user.to_dict()

        return make_response(jsonify(new_user_dict), 201)

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}, 200
        else:
            return {'message': 'User not found'}, 404

    update_user_model = api.model('UpdateUser', {
        'username': fields.String(description='Updated username'),
        'email': fields.String(description='Updated email'),
        'phone_number': fields.String(description='Updated phone number'),
        'role_id': fields.Integer(description='Updated role ID'),
    })

    @api.expect(update_user_model)
    def put(self, user_id):
        user = User.query.get(user_id)
        if user:
            data = request.get_json()
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.phone_number = data.get('phone_number', user.phone_number)
            user.role_id = data.get('role_id', user.role_id)

            db.session.commit()
            updated_user_data = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'phone_number': user.phone_number,
                'role_id': user.role_id,
            }
            return {'message': 'User updated successfully', 'updated_user': updated_user_data}, 200
        else:
            return {'message': 'User not found'}, 404
api.add_resource(UserResource, '/users', '/users/<int:user_id>', endpoint='users')

        
@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        "Not Found:The requested endpoint(resource) does not exist",
        404
        )
    return response


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
