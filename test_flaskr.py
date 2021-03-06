import os
import json
import unittest

from flaskr import create_app
from flaskr.models import setup_db, User


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        # its better to use another database for testing, but here to make things simple I am using the same database
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

    def test_update_user_name(self):
        res = self.client().patch('/users/3', json={'name': 'Brad'})
        data = json.loads(res.data)
        user = User.query.filter(User.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(user.name, 'Brad')

    def test_400_failed_update(self):
        res = self.client().patch('/users/3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_create_user(self):
        res = self.client().post('/users', json=self.new_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['users']))

    def test_if_user_creation_not_allowed(self):
        res = self.client().post('/users/32', json=self.new_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_delete_user(self):
        res = self.client().delete('/users/12')
        data = json.loads(res.data)
        user = User.query.filter(User.id == 12).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 12)
        self.assertTrue(data['total_users'])
        self.assertTrue(len(data['users']))
        self.assertEqual(user, None)

    def test_422_if_user_does_not_exist(self):
        res = self.client().delete('users/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_search_users_with_results(self):
        res = self.client().post('/users/search', json={'name': 'Ryan'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_users'])
        self.assertEqual(len(data['users']), 1)

    def test_search_users_without_results(self):
        res = self.client().post('/users/search', json={'name': 'fjgdfhgjdhk'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_users'], 0)
        self.assertEqual(len(data['users']), 0)


if __name__ == "__main__":
    unittest.main()
