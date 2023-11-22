# from flask import Flask
from flask_migrate import Migrate
from flask import Flask,jsonify,request,make_response
from flask_restful import Api,Resource
from werkzeug.exceptions import NotFound
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import db,Event, Payment, Role, Category
# from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import random
import string

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR']=True
# migrate = Migrate(app.db)
db.init_app(app)
migrate = Migrate(app, db)


api = Api(app)
CORS (app)


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
    db.create_all()
    app.run(debug=True)

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)