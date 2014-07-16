#!/usr/bin/env python

import base64
from . import IgorApiTestCase
from flask import url_for
from endpoints import * 

class LoginTestCase(IgorApiTestCase):

    def test_root(self):
        # / should be accessible without logging in
        self.assert_200(self.client.get(url_for('root')))

    def test_login(self):

        # No credentials provided
        self.assert_401(self.client.get(url_for('login')))

        # Incorrect username
        self.assert_401(self.client.get(url_for('login'),
                        headers=[('Authorization', 'Basic '
                                                  + base64.b64encode('toor:root'))]))

        # Incorrect password
        self.assert_401(self.client.get(url_for('login'),
                        headers=[('Authorization', 'Basic '
                                                  + base64.b64encode('root:toor'))]))

        # Incorrect username and password
        self.assert_401(self.client.get(url_for('login'),
                        headers=[('Authorization', 'Basic '
                                                  + base64.b64encode('toor:toor'))]))
        
        # Correct username and password
        self.assert_200(self.client.get(url_for('login'),
                        headers=[('Authorization', 'Basic '
                                                  + base64.b64encode('root:root'))]))

    def test_unauthenticated_endpoints(self):
        # Should not be able to access any endpoints without authentication
        for endpoint in all_endpoints:
            self.assert_401(self.client.get(url_for(endpoint,
                                                    username='username',
                                                    hostname='hostname',
                                                    channel=0)))
