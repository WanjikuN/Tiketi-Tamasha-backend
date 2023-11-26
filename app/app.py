# from flask import Flask
from flask_migrate import Migrate
from flask import Flask,jsonify,request,make_response
from flask_restful import Api,Resource
from werkzeug.exceptions import NotFound
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from models import db,Event, Payment, Role, Category
# from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import random
import string
# Daraja
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import base64

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR']=True
# migrate = Migrate(app.db)
db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)
CORS(app)
CORS(app, resources={r"/lnmo": {"origins": "http://localhost:3000"}})

base_url = 'https://77fb-41-90-66-250.ngrok-free.app'
consumer_keys = 'TKbOPVqsnYJpiDvQNlcQlMQP5P1Ch2c0'
consumer_secrets = 'YG2R7UVJfKtj8MkK'


class Stk_Push(Resource):
    @cross_origin(supports_credentials=True)
    def get(self):
        amount =request.args.get('amount')
        phone = request.args.get('phone')

        endpoint = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

        access_token = _access_token()
        headers = { "Authorization": "Bearer %s" % access_token }
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

        res = requests.post(endpoint, json = data, headers = headers)
        return res.json()


    @cross_origin(supports_credentials=True)
    def post(self):
        data = request.get_data()
        print(data)

        # Decode bytes to string
        decoded_data = data.decode('utf-8')

        # Parse the JSON data
        try:
            json_data = json.loads(decoded_data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return 'Error decoding JSON'

        # Access the 'Item' list under 'CallbackMetadata'
        result_code = json_data.get('Body', {}).get('stkCallback', {}).get('ResultCode')

        items = json_data.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata', {}).get('Item', [])
        if result_code == 0:
            
            for item in items:
                name = item.get('Name')
                value = item.get('Value')
                print(f"Name: {name}, Value: {value}")
        # 'a' (append) mode
        else:
            
            print(f"Payment failed. Result Code: {result_code}")

        with open('lnmo.json', 'a') as f:
            f.write(decoded_data)
        return jsonify({"Result": "ok"})

def _access_token():
        consumer_key = consumer_keys
        consumer_secret = consumer_secrets
        endpoint = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

        r = requests.get(endpoint, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        data = r.json()
        return data['access_token']
    
api.add_resource(Stk_Push, '/lnmo', endpoint='lnmo')
class Eventors(Resource):
    def get(self):
        even_dict=[n.to_dict() for n in Event.query.all()]
        response = make_response(
            jsonify(even_dict),200
        )
        return response
    

    def post(self):
        data = request.get_json()        
        newrec= Event(
            event=data.get('event'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            location=data.get('location'),
            description=data.get('description'),
            mvp_price=data.get('mvp_price'),
            regular_price=data.get('regular_price'),
            Early_booking_price=data.get('Early_booking_price'),
        )
    def delete(self, event_id):
        
        event = Event.query.get(event_id)
        if event:
            db.session.delete(event)
            db.session.commit()
            return {'message': 'Event deleted successfully'}, 200
        else:
            return {'message': 'Event not found'}, 404

    def put(self, event_id):
        
        event = Event.query.get(event_id)
        if event:
            data = request.get_json()
            event.event = data.get('event', event.event)
            event.start_time = data.get('start_time', event.start_time)
            
            db.session.commit()
            return {'message': 'Event updated successfully'}, 200
        else:
            return {'message': 'Event not found'}, 404    

        db.session.add(newrec)
        db.session.commit() 

        newrec_dict=newrec.to_dict()

        response=make_response(jsonify(newrec_dict))
        response.content_type='application/json'

        return response
    
api.add_resource(Eventors, '/events', endpoint='events')
    
class PaymentResource(Resource):
    def get(self):
        payments = Payment.query.all()
        payment_dict = [payment.to_dict() for payment in payments]
        return make_response(jsonify(payment_dict), 200)

    def post(self):
        data = request.get_json()
        
        new_payment = Payment(
            payment_type=data.get('payment_type'),
            payment_date=data.get('payment_date'),
            user_id=data.get('user_id'),
            status=data.get('status'),
            event_id=data.get('event_id'),
        )
    def delete(self, payment_id):
        payment = Payment.query.get(payment_id)
        if payment:
            db.session.delete(payment)
            db.session.commit()
            return {'message': 'Payment deleted successfully'}, 200
        else:
            return {'message': 'Payment not found'}, 404

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

        db.session.add(new_payment)
        db.session.commit()

        new_payment_dict = new_payment.to_dict()
        return make_response(jsonify(new_payment_dict), 201)

api.add_resource(PaymentResource, '/payments', endpoint='payments')


class RoleResource(Resource):
    def get(self):
        roles = Role.query.all()
        role_dict = [role.to_dict() for role in roles]
        return make_response(jsonify(role_dict), 200)

    def post(self):
        data = request.get_json()
        
        new_role = Role(
            role_name=data.get('role_name'),
            description=data.get('description'),
            
        )
    def delete(self, role_id):
        role = Role.query.get(role_id)
        if role:
            db.session.delete(role)
            db.session.commit()
            return {'message': 'Role deleted successfully'}, 200
        else:
            return {'message': 'Role not found'}, 404

    def put(self, role_id):
        role = Role.query.get(role_id)
        if role:
            data = request.get_json()
            role.role_name = data.get('role_name', role.role_name)
            role.description = data.get('description', role.description)
           
            db.session.commit()
            return {'message': 'Role updated successfully'}, 200
        else:
            return {'message': 'Role not found'}, 404
        db.session.add(new_role)
        db.session.commit()

        new_role_dict = new_role.to_dict()
        return make_response(jsonify(new_role_dict), 201)

api.add_resource(RoleResource, '/roles', endpoint='roles')


class CategoryResource(Resource):
    def get(self):
        categories = Category.query.all()
        category_dict = [category.to_dict() for category in categories]
        return make_response(jsonify(category_dict), 200)

    def post(self):
        data = request.get_json()
        
        new_category = Category(
            category_name=data.get('category_name'),
            event_id=data.get('event_id'),        
        )
    def delete(self, category_id):
        category = Category.query.get(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
            return {'message': 'Category deleted successfully'}, 200
        else:
            return {'message': 'Category not found'}, 404

    def put(self, category_id):
        category = Category.query.get(category_id)
        if category:
            data = request.get_json()
            category.category_name = data.get('category_name', category.category_name)
            category.event_id = data.get('event_id', category.event_id)
            
            db.session.commit()
            return {'message': 'Category updated successfully'}, 200
        else:
            return {'message': 'Category not found'}, 404
        db.session.add(new_category)
        db.session.commit()

        new_category_dict = new_category.to_dict()
        return make_response(jsonify(new_category_dict), 201)

api.add_resource(CategoryResource, '/categories', endpoint='categories')

        
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

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)