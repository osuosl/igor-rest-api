#!/usr/bin/env python

import base64
import json
from flask import url_for

from . import IgorApiTestCase
from igor_rest_api.config import ROOT_USER, ROOT_PASS
from igor_rest_api.api.grouping.models import Userdetails

class GroupingUsersTestCase(IgorApiTestCase):

    test_user = 'test_user'
    test_pass = 'test_pass'

    def setUp(self):
        # Login as ROOT_USER prior to all test cases
        super(GroupingUsersTestCase, self).setUp()
        response = self.client.get(url_for('groupingslogin'),
                                   headers=[('Authorization', 'Basic '
                                             + base64.b64encode(ROOT_USER +
                                                                ':' +
                                                                ROOT_PASS))])
        self.headers = [('Authorization', 'Basic '
                         + base64.b64encode((response.json)['token']
                         + ':' + ROOT_USER)),
                        ('Content-Type', 'application/json')]

    def create_test_user(self):
        user = Userdetails(self.test_user, self.test_pass)
        self.db.session.add(user)
        self.db.session.commit()

    def test_list_users(self):
        self.create_test_user()

        response = self.client.get(url_for('groupingsusers'), headers=self.headers)
        self.assert_200(response)

        users = (response.json)['users']
        usernames = [user['userid'] for user in users]

        self.assertIn(1, usernames, 'root not in user list')
        self.assertIn(2, usernames, 'test_user not in user list')
        self.assertEqual(2, len(usernames), 'unexpected number of users')

    def test_login_user(self):
        self.create_test_user()

        response = self.client.get(url_for('groupingslogin'),
                                   headers=[('Authorization', 'Basic '
                                        + base64.b64encode(self.test_user +
                                                           ':' +
                                                           self.test_pass))])
        self.assert_200(response)

    def test_add_user(self):
        expected_new_user_response = {u'username': self.test_user,
                                      u'location': url_for('groupingsuser',
                                                    userid=2,
                                                    _external=True)}

        data = json.dumps({'username': self.test_user,
                           'password': self.test_pass})

        response = self.client.post(url_for('groupingsusers'),
                                    data=data,
                                    headers=self.headers)
        self.assertStatus(response, 201)
        self.assertEqual(response.json, expected_new_user_response,
                         'Unexpected response when adding a new user')

        user = Userdetails.query.filter_by(username=self.test_user).first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password(self.test_pass))

    def test_add_existing_user(self):
        self.create_test_user()

        expected_existing_user_response = {u'message': u'User %s exists'
                                                       % self.test_user}

        data = json.dumps({'username': self.test_user,
                           'password': 'new_pass'})

        response = self.client.post(url_for('groupingsusers'),
                                    data=data,
                                    headers=self.headers)
        self.assert_400(response)
        self.assertEqual(response.json, expected_existing_user_response,
                         'Unexpected response when adding an existing user')

    def test_user_info(self):
        self.create_test_user()

        expected_user_info = {u'username': self.test_user,
                               'userid' : 2,
                              u'location': url_for('groupingsuser',
                                                   userid=2,
                                                   _external=True),}

        response = self.client.get(url_for('groupingsuser', userid=2),
                                   headers=self.headers)
        self.assert_200(response)
        print response.json
        self.assertEqual(response.json, expected_user_info,
                        'Unexpected user info after adding user')

    def test_nonexistent_user_info(self):
        response = self.client.get(url_for('groupingsuser', userid=2345),
                                   headers=self.headers)
        self.assert_404(response)

    def test_remove_root_user(self):
        self.create_test_user()
        response = self.client.delete(url_for('groupingsuser',
                                              userid=1),
                                      headers=[('Authorization', 'Basic '
                                        + base64.b64encode(self.test_user +
                                                           ':' +
                                                           self.test_pass))])
        self.assert_400(response)

    def test_remove_user(self):
        self.create_test_user()
        response = self.client.delete(url_for('groupingsuser',
                                              userid=2),
                                      headers=self.headers)
        self.assert_200(response)

        user = Userdetails.query.filter_by(username=self.test_user).first()
        self.assertIsNone(user)

    def test_remove_nonexistent_user(self):
        response = self.client.delete(url_for('user', username='something'),
                                      headers=self.headers)
        self.assert_404(response)

    def test_update_user(self):
        self.create_test_user()

        data = json.dumps({'password': 'newpass'})

        response = self.client.post(url_for('groupingsuser', userid=2),
                                   data=data,
                                   headers=self.headers)
        self.assert_200(response)

        user = Userdetails.query.filter_by(username=self.test_user).first()
        self.assertTrue(user.check_password('newpass'))
