#!/usr/bin/env python

import base64
import json
from flask import url_for

from . import IgorApiTestCase
from igor_rest_api.config import ROOT_USER, ROOT_PASS
from igor_rest_api.api.snmp.models import Snmpuser 
from igor_rest_api.api.pdus.models import Pdu

class PermissionsTestCase(IgorApiTestCase):

    test_host = 'test_host'
    test_ip = 'test_ip'
    test_user = 'test_user' # Reused for test user
    test_pass = 'test_pass' # Reused for test user

    def setUp(self):
        # Login as ROOT_USER prior to all test cases
        super(PermissionsTestCase, self).setUp()
        response = self.client.get(url_for('snmplogin'),
                                   headers=[('Authorization', 'Basic '
                                             + base64.b64encode(ROOT_USER +
                                                                ':' +
                                                                ROOT_PASS))])
        self.headers = [('Authorization', 'Basic '
                         + base64.b64encode((response.json)['token']
                         + ':' + ROOT_USER)),
                        ('Content-Type', 'application/json')]

    def create_test_pdu(self, ip='test_ip',hostname=test_host):
        pdu = Pdu(hostname, ip,
                           self.test_pass)
        self.db.session.add(pdu)
        self.db.session.commit()
        return pdu 

    def create_test_user(self, username='test_user'):
        user = Snmpuser(username, self.test_pass)
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def test_list_user_pdus(self):
        user = self.create_test_user()

        response = self.client.get(url_for('user_pdus',
                                            username=user.username),
                                   headers=self.headers)
        self.assert_200(response)
        self.assertEquals(0, len((response.json)['pdus']),
                          'no permissions should exist before grant')

        pdu1 = self.create_test_pdu(ip='pdu_one',hostname='host1')
        pdu2 = self.create_test_pdu(ip='pdu_two',hostname='host2')
        user.pdus.extend([pdu1, pdu2])

        self.db.session.add(user)
        self.db.session.commit()

        response = self.client.get(url_for('user_pdus',
                                            username=self.test_user),
                                   headers=self.headers)
        self.assert_200(response)

        pdus = [pdu['ip'] for pdu in
                    (response.json)['pdus']]

        self.assertIn(pdu1.ip, pdus)
        self.assertIn(pdu2.ip, pdus)
        self.assertEquals(2, len(pdus))

    def test_list_pdu_users(self):
        pdu = self.create_test_pdu()

        response = self.client.get(url_for('pdu_users',
                                            ip=pdu.ip),
                                   headers=self.headers)
        self.assert_200(response)
        self.assertEquals(0, len((response.json)['users']),
                          'no permissions should exist before grant')

        user1 = self.create_test_user(username='user_one')
        user2 = self.create_test_user(username='user_two')
        pdu.users.extend([user1, user2])

        self.db.session.add(pdu)
        self.db.session.commit()

        response = self.client.get(url_for('pdu_users',
                                            ip=self.test_ip),
                                   headers=self.headers)
        self.assert_200(response)

        users = [user['username'] for user in
                (response.json)['users']]

        self.assertIn(user1.username, users)
        self.assertIn(user2.username, users)
        self.assertEquals(2, len(users))

    def test_add_pdu_to_user(self):
        user = self.create_test_user()
        pdu = self.create_test_pdu()

        response = self.client.put(url_for('user_pdu',
                                            username=user.username,
                                            ip=pdu.ip),
                                   headers=self.headers)
        self.assertStatus(response, 201)

        user2 = Snmpuser.query.filter_by(username=user.username).first()
        self.assertIn(pdu, user2.pdus,
                      'expected pdu to exist for user')

    def test_add_user_to_pdu(self):
        user = self.create_test_user()
        pdu = self.create_test_pdu()

        response = self.client.put(url_for('pdu_user',
                                            username=user.username,
                                            ip=pdu.ip),
                                   headers=self.headers)
        self.assertStatus(response, 201)

        pdu2 = Pdu.query.filter_by(ip=pdu.ip).first()
        self.assertIn(user, pdu2.users,
                      'expected user to exist for machine')

    def test_check_pdu_for_user(self):
        pdu = self.create_test_pdu()
        user = self.create_test_user()

        response = self.client.get(url_for('user_pdu',
                                            username=user.username,
                                            ip=pdu.ip),
                                   headers=self.headers)
        self.assert_404(response, 'user must not have permission for pdu')

        user.pdus.append(pdu)
        self.db.session.add(user)
        self.db.session.commit()

        response = self.client.get(url_for('user_pdu',
                                            username=user.username,
                                            ip=pdu.ip),
                                   headers=self.headers)
        self.assert_200(response, 'user must have permission for pdu')

    def test_check_user_for_pdu(self):
        pdu = self.create_test_pdu()
        user = self.create_test_user()

        response = self.client.get(url_for('pdu_user',
                                            username=user.username,
                                            ip=pdu.ip),
                                   headers=self.headers)
        self.assert_404(response, 'user must not have permission for pdu')

        pdu.users.append(user)
        self.db.session.add(pdu)
        self.db.session.commit()


        url = url_for('pdu_user',username=user.username,ip=pdu.ip)
        response = self.client.get(url,headers=self.headers)
        print response
        """
        response = self.client.get(url_for('pdu_user',
                                            username=user.username,
                                            ip=pdu.ip),
                                   headers=self.headers)
                                   """
        self.assert_200(response, 'user must have permission for pdu')

    def test_remove_pdu_from_user(self):
        pdu = self.create_test_pdu()
        user = self.create_test_user()

        user.pdus.append(pdu)
        self.db.session.add(user)
        self.db.session.commit()

        response = self.client.delete(url_for('user_pdu',
                                               username=user.username,
                                               ip=pdu.ip),
                                      headers=self.headers)
        self.assert_200(response, 'unexpected error revoking permission')

        user2 = Snmpuser.query.filter_by(username=user.username).first()
        self.assertEquals(0, len(user2.pdus))

    def test_remove_user_from_pdu(self):
        pdu = self.create_test_pdu()
        user = self.create_test_user()

        pdu.users.append(user)
        self.db.session.add(pdu)
        self.db.session.commit()

        response = self.client.delete(url_for('pdu_user',
                                               username=user.username,
                                               ip=pdu.ip),
                                      headers=self.headers)
        self.assert_200(response, 'unexpected error revoking permission')

        pdu2 = Pdu.query.filter_by(ip=pdu.ip).first()
        self.assertEquals(0, len(pdu2.users))
