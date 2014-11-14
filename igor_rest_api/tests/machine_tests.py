#!/usr/bin/env python

import base64
import json
from flask import url_for

from . import IgorApiTestCase
from igor_rest_api.config import ROOT_USER, ROOT_PASS
from igor_rest_api.api.machines.models import Machine

class MachinesTestCase(IgorApiTestCase):

    test_host = 'test_host'
    test_fqdn = 'test_fqdn'
    test_user = 'test_user'
    test_pass = 'test_pass'

    def setUp(self):
        # Login as ROOT_USER prior to all test cases
        super(MachinesTestCase, self).setUp()
        response = self.client.get(url_for('login'),
                                   headers=[('Authorization', 'Basic '
                                             + base64.b64encode(ROOT_USER +
                                                                ':' +
                                                                ROOT_PASS))])
        self.headers = [('Authorization', 'Basic '
                         + base64.b64encode((response.json)['token']
                         + ':' + ROOT_USER)),
                        ('Content-Type', 'application/json')]

    def create_test_machine(self):
        machine = Machine(self.test_host, self.test_fqdn,
                          self.test_user, self.test_pass)
        self.db.session.add(machine)
        self.db.session.commit()

    def test_list_machines(self):
        self.create_test_machine()

        response = self.client.get(url_for('machines'), headers=self.headers)
        self.assert_200(response)

        machine = (response.json)['machines'][0]
        self.assertEqual(self.test_host, machine['hostname'],
                         'unexpected machine hostname')

    def test_add_machine(self):
        data = json.dumps({'hostname': self.test_host,
                           'fqdn': self.test_fqdn,
                           'username': self.test_user,
                           'password': self.test_pass})

        response = self.client.post(url_for('machines'),
                                    data=data,
                                    headers=self.headers)
        self.assertStatus(response, 201)

        machine = Machine.query.filter_by(hostname=self.test_host).first()
        self.assertIsNotNone(machine)
        self.assertEqual(self.test_fqdn, machine.fqdn)
        self.assertEqual(self.test_user, machine.username)
        self.assertEqual(self.test_pass, machine.password)

    def test_add_existing_machine(self):
        self.create_test_machine()

        expected_existing_user_response = {u'message': u'Host %s exists'
                                                       % self.test_host}

        data = json.dumps({'hostname': self.test_host,
                           'fqdn': 'new_fqdn',
                           'username': 'new_user',
                           'password': 'new_pass'})

        response = self.client.post(url_for('machines'),
                                    data=data,
                                    headers=self.headers)
        self.assert_400(response)
        self.assertEqual(response.json, expected_existing_user_response,
                         'Unexpected response when adding an existing machine')

    def test_machine_info(self):
        self.create_test_machine()

        response = self.client.get(url_for('machine',
                                            hostname=self.test_host),
                                   headers=self.headers)
        self.assert_200(response)

        machine = response.json
        self.assertEqual(self.test_host, machine['hostname'],
                         'unexpected machine hostname')
        self.assertEqual(self.test_fqdn, machine['fqdn'],
                         'unexpected machine fqdn')

    def test_nonexistent_machine_info(self):
        response = self.client.get(url_for('machine', hostname='something'),
                                   headers=self.headers)
        self.assert_404(response)

    def test_remove_user(self):
        self.create_test_machine()
        response = self.client.delete(url_for('machine',
                                              hostname=self.test_host),
                                      headers=self.headers)
        self.assert_200(response)

        machine = Machine.query.filter_by(hostname=self.test_host).first()
        self.assertIsNone(machine)

    def test_remove_nonexistent_machine(self):
        response = self.client.delete(url_for('machine', hostname='something'),
                                      headers=self.headers)
        self.assert_404(response)

    def test_update_machine(self):
        self.create_test_machine()

        new_fqdn = 'new_fqdn'
        new_user = 'new_user'
        new_pass = 'new_pass'

        data = json.dumps({'fqdn': new_fqdn,
                           'username': new_user,
                           'password': new_pass})

        response = self.client.put(url_for('machine',
                                            hostname=self.test_host),
                                   headers=self.headers, data=data)
        self.assert_200(response)

        machine = Machine.query.filter_by(hostname=
                                          self.test_host).first()
        self.assertIsNotNone(machine)
        self.assertEqual(new_fqdn, machine.fqdn)
        self.assertEqual(new_user, machine.username)
        self.assertEqual(new_pass, machine.password)
