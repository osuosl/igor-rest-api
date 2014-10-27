#!/usr/bin/env python

import base64
from flask import url_for

from . import IgorApiTestCase
from igor_rest_api.api.routes import resources

class LoginTestCase(IgorApiTestCase):

    def test_root(self):
        self.assert_200(self.client.get(url_for('root')),
                        message='root must be accessible without login')

    def test_login(self):

        self.assert_401(self.client.get(url_for('login')),
                        message='login should fail without credentials')

        self.assert_401(self.client.get(url_for('login'),
                        headers=[('Authorization', 'Basic '
                                    + base64.b64encode('toor:root'))]),
                        message='login should fail with incorrect username')

        self.assert_401(self.client.get(url_for('login'),
                        headers=[('Authorization', 'Basic '
                                    + base64.b64encode('root:toor'))]),
                        message='login should fail with incorrect password')

        self.assert_401(self.client.get(url_for('login'),
                        headers=[('Authorization', 'Basic '
                                    + base64.b64encode('toor:toor'))]),
                        message='login should fail with wrong username/pass')

        self.assert_200(self.client.get(url_for('login'),
                        headers=[('Authorization', 'Basic '
                                    + base64.b64encode('root:root'))]),
                        message='login should pass with correct username/pass')

    def test_unauthenticated_endpoints(self):
        for resource in resources:
            resourceClass, url, endpoint = resource

            if endpoint == 'root':
                continue

            endpoint_url = url_for(endpoint,
                                   username='username',
                                   hostname='hostname',
                                   sensor='sensor',
                                   channel=0)

            self.assert_401(self.client.get(endpoint_url),
                            message=endpoint_url +
                            ' should be inaccessible without login')
