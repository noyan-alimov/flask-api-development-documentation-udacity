import os
import json
import unittest

from flaskr import create_app
from flaskr.models import setup_db, User


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        self.new_user = {
            'name': 'Jenny',
            'email': 'jenny@mail.com'
        }

    def tearDown(self):
        pass

    def test_get_paginated_users(self):
        res = self.client().get('/users')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_users'])
        self.assertTrue(len(data['users']))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/users?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


if __name__ == "__main__":
    unittest.main()
