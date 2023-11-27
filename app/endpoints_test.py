import unittest
from flask import Flask
from flask_testing import TestCase
from app import Eventors, db, app

class TestEventorsResource(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection in testing
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
        app.config['DEBUG'] = False  # Set to True to enable detailed error messages
        app.config['PROPAGATE_EXCEPTIONS'] = True

        db.init_app(app)
        
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_all_events(self):
        response = self.client.get('/events')
        self.assert404(response)
        self.assertEqual(response.json, [])

    def test_get_single_event(self):
        response = self.client.get('/events/1')
        self.assert404(response)
        self.assertEqual(response.json, {"message": "Event not found"})

    def test_get_single_event_not_found(self):
        response = self.client.get('/events/999')
        self.assert404(response)
        self.assertEqual(response.json, {"message": "Event not found"})

if __name__ == '__main__':
    unittest.main()


