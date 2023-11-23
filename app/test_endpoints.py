import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db

class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        self.app_context.pop()

    # Helper function to create test data
    def create_event(self, event_name, start_time, end_time, location, description, MVP_price, regular_price, early_booking_price):
        return self.app.post('/events', json={
            'event_name': event_name,
            'start_time': start_time,
            'end_time': end_time,
            'location': location,
            'description': description,
            'MVP_price': MVP_price,
            'regular_price': regular_price,
            'early_booking_price': early_booking_price
        })

    def test_create_event(self):
        response = self.create_event('Test Event', '2023-01-01T00:00:00', '2023-01-01T01:00:00', 'Test Location', 'Test Description', 100.0, 50.0, 75.0)
        self.assertEqual(response.status_code, 200)

    def test_get_events(self):
        self.create_event('Event 1', '2023-01-01T00:00:00', '2023-01-01T01:00:00', 'Location 1', 'Description 1', 100.0, 50.0, 75.0)
        self.create_event('Event 2', '2023-01-02T00:00:00', '2023-01-02T01:00:00', 'Location 2', 'Description 2', 120.0, 60.0, 90.0)

        response = self.app.get('/events')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 2)

    def test_update_event(self):
        create_response = self.create_event('EventToUpdate', '2023-01-01T00:00:00', '2023-01-01T01:00:00', 'LocationToUpdate', 'DescriptionToUpdate', 100.0, 50.0, 75.0)
        event_id = create_response.json['id']

        response = self.app.put(f'/events/{event_id}', json={
            'event_name': 'UpdatedEvent',
            'start_time': '2023-02-01T00:00:00',
            'end_time': '2023-02-01T01:00:00',
            'location': 'UpdatedLocation',
            'description': 'UpdatedDescription',
            'MVP_price': 120.0,
            'regular_price': 60.0,
            'early_booking_price': 90.0
        })

        self.assertEqual(response.status_code, 200)

    def test_delete_event(self):
        create_response = self.create_event('EventToDelete', '2023-01-01T00:00:00', '2023-01-01T01:00:00', 'LocationToDelete', 'DescriptionToDelete', 100.0, 50.0, 75.0)
        event_id = create_response.json['id']

        response = self.app.delete(f'/events/{event_id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
