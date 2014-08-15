#!/usr/bin/env python

import base64
import json
from . import IgorApiTestCase
from flask import url_for
from config import ROOT_USER, ROOT_PASS
from api.models import User, Machine

class PermissionsTestCase(IgorApiTestCase):

    test_host = 'test_host'
    test_fqdn = 'test_fqdn'
    test_user = 'test_user' # Reused for test user
    test_pass = 'test_pass' # Reused for test user

    def setUp(self):
        # Login as ROOT_USER prior to all test cases
        super(PermissionsTestCase, self).setUp()
        response = self.client.get(url_for('login'),
                                   headers=[('Authorization', 'Basic '
                                             + base64.b64encode(ROOT_USER +
                                                                ':' +
                                                                ROOT_PASS))])
        self.headers = [('Authorization', 'Basic '
                         + base64.b64encode((response.json)['token']
                         + ':' + ROOT_USER)),
                        ('Content-Type', 'application/json')]

    def create_test_machine(self, hostname='test_host'):
        machine = Machine(hostname, hostname,
                          self.test_user, self.test_pass)
        self.db.session.add(machine)
        self.db.session.commit()
        return machine

    def create_test_user(self, username='test_user'):
        user = User(username, self.test_pass)
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def test_list_user_machines(self):
        user = self.create_test_user()

        response = self.client.get(url_for('user_machines',
                                            username=user.username),
                                   headers=self.headers)
        self.assert_200(response)
        self.assertEquals(0, len((response.json)['machines']),
                          'no permissions should exist before grant')

        machine1 = self.create_test_machine(hostname='machine_one')
        machine2 = self.create_test_machine(hostname='machine_two')
        user.machines.extend([machine1, machine2])

        self.db.session.add(user)
        self.db.session.commit()

        response = self.client.get(url_for('user_machines',
                                            username=self.test_user),
                                   headers=self.headers)
        self.assert_200(response)

        machines = [machine['hostname'] for machine in
                    (response.json)['machines']]

        self.assertIn(machine1.hostname, machines)
        self.assertIn(machine2.hostname, machines)
        self.assertEquals(2, len(machines))

    def test_list_machine_users(self):
        machine = self.create_test_machine()

        response = self.client.get(url_for('machine_users',
                                            hostname=machine.hostname),
                                   headers=self.headers)
        self.assert_200(response)
        self.assertEquals(0, len((response.json)['users']),
                          'no permissions should exist before grant')
        
        user1 = self.create_test_user(username='user_one')
        user2 = self.create_test_user(username='user_two')
        machine.users.extend([user1, user2])

        self.db.session.add(machine)
        self.db.session.commit()

        response = self.client.get(url_for('machine_users',
                                            hostname=self.test_host),
                                   headers=self.headers)
        self.assert_200(response)

        users = [user['username'] for user in
                (response.json)['users']]

        self.assertIn(user1.username, users)
        self.assertIn(user2.username, users)
        self.assertEquals(2, len(users))

    def test_add_machine_to_user(self):
        user = self.create_test_user()
        machine = self.create_test_machine()

        response = self.client.put(url_for('user_machine',
                                            username=user.username,
                                            hostname=machine.hostname),
                                   headers=self.headers)
        self.assertStatus(response, 201)

        user2 = User.query.filter_by(username=user.username).first()
        self.assertIn(machine, user2.machines,
                      'expected machine to exist for user')

    def test_add_user_to_machine(self):
        user = self.create_test_user()
        machine = self.create_test_machine()

        response = self.client.put(url_for('machine_user',
                                            username=user.username,
                                            hostname=machine.hostname),
                                   headers=self.headers)
        self.assertStatus(response, 201)

        machine2 = Machine.query.filter_by(hostname=machine.hostname).first()
        self.assertIn(user, machine2.users,
                      'expected user to exist for machine')

    def test_check_machine_for_user(self):
        machine = self.create_test_machine()
        user = self.create_test_user()
        
        response = self.client.get(url_for('user_machine',
                                            username=user.username,
                                            hostname=machine.hostname),
                                   headers=self.headers)
        self.assert_404(response, 'user must not have permission for machine')

        user.machines.append(machine)
        self.db.session.add(user)
        self.db.session.commit()
        
        response = self.client.get(url_for('user_machine',
                                            username=user.username,
                                            hostname=machine.hostname),
                                   headers=self.headers)
        self.assert_200(response, 'user must have permission for machine')

    def test_check_user_for_machine(self):
        machine = self.create_test_machine()
        user = self.create_test_user()

        response = self.client.get(url_for('machine_user',
                                            username=user.username,
                                            hostname=machine.hostname),
                                   headers=self.headers)
        self.assert_404(response, 'user must not have permission for machine')

        machine.users.append(user)
        self.db.session.add(machine)
        self.db.session.commit()
        
        response = self.client.get(url_for('machine_user',
                                            username=user.username,
                                            hostname=machine.hostname),
                                   headers=self.headers)
        self.assert_200(response, 'user must have permission for machine')

    def test_remove_machine_from_user(self):
        machine = self.create_test_machine()
        user = self.create_test_user()
        
        user.machines.append(machine)
        self.db.session.add(user)
        self.db.session.commit()

        response = self.client.delete(url_for('user_machine',
                                               username=user.username,
                                               hostname=machine.hostname),
                                      headers=self.headers)
        self.assert_200(response, 'unexpected error revoking permission')
        
        user2 = User.query.filter_by(username=user.username).first()
        self.assertEquals(0, len(user2.machines))
    
    def test_remove_user_from_machine(self):
        machine = self.create_test_machine()
        user = self.create_test_user()
        
        machine.users.append(user)
        self.db.session.add(machine)
        self.db.session.commit()
        
        response = self.client.delete(url_for('machine_user',
                                               username=user.username,
                                               hostname=machine.hostname),
                                      headers=self.headers)
        self.assert_200(response, 'unexpected error revoking permission')
        
        machine2 = Machine.query.filter_by(hostname=machine.hostname).first()
        self.assertEquals(0, len(machine2.users))
