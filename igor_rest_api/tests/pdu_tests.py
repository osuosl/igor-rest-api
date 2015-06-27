#!/usr/bin/env python

import base64
import json
from flask import url_for

from . import IgorApiTestCase
from igor_rest_api.config import ROOT_USER, ROOT_PASS
from igor_rest_api.api.pdus.models import Pdu

class PdusTestCase(IgorApiTestCase):

    test_host = 'test_host'
    test_ip = 'test_ip'
    test_pass = 'test_pass'

    def setUp(self):
        # Login as ROOT_USER prior to all test cases
        super(PdusTestCase, self).setUp()
        response = self.client.get(url_for('login'),
                                   headers=[('Authorization', 'Basic '
                                             + base64.b64encode(ROOT_USER +
                                                                ':' +
                                                                ROOT_PASS))])
        self.headers = [('Authorization', 'Basic '
                         + base64.b64encode((response.json)['token']
                         + ':' + ROOT_USER)),
                        ('Content-Type', 'application/json')]

    def create_test_pdu(self):
        pdu = Pdu(self.test_host, self.test_ip, self.test_pass)
        self.db.session.add(pdu)
        self.db.session.commit()

    def test_list_pdus(self):
        self.create_test_pdu()

        response = self.client.get(url_for('pdus'), headers=self.headers)
        self.assert_200(response)

        pdu = (response.json)['pdus'][0]
        self.assertEqual(self.test_ip, pdu['ip'],
                         'unexpected pdu ip')

    def test_add_pdu(self):
        data = json.dumps({'hostname': self.test_host,
                           'ip': self.test_ip,
                           'password': self.test_pass})

        response = self.client.post(url_for('pdus'),
                                    data=data,
                                    headers=self.headers)
        self.assertStatus(response, 201)

        pdu = Pdu.query.filter_by(hostname=self.test_host).first()
        self.assertIsNotNone(pdu)
        self.assertEqual(self.test_ip, pdu.ip)
        self.assertEqual(self.test_pass, pdu.password)

    def test_add_existing_pdu(self):
        self.create_test_pdu()

        new_hostname = 'new_hostname'
        expected_existing_user_response = {u'message': u'Host %s exists'
                                                       % new_hostname}

        data = json.dumps({'hostname': new_hostname,
                           'ip': self.test_ip,
                           'password': 'new_pass'})

        response = self.client.post(url_for('pdus'),
                                    data=data,
                                    headers=self.headers)
        print response.json
        self.assert_400(response)
        self.assertEqual(response.json, expected_existing_user_response,
                         'Unexpected response when adding an existing pdu')

    def test_pdu_info(self):
        self.create_test_pdu()

        response = self.client.get(url_for('pdu',
                                            ip=self.test_ip),
                                   headers=self.headers)
        self.assert_200(response)

        pdu = response.json
        self.assertEqual(self.test_host, pdu['hostname'],
                         'unexpected pdu hostname')
        self.assertEqual(self.test_ip, pdu['ip'],
                         'unexpected pdu ip')

    def test_nonexistent_pdu_info(self):
        response = self.client.get(url_for('pdu', ip='something'),
                                   headers=self.headers)
        self.assert_404(response)

    def test_remove_user(self):
        self.create_test_pdu()
        response = self.client.delete(url_for('pdu',
                                              ip=self.test_ip),
                                      headers=self.headers)
        self.assert_200(response)

        pdu = Pdu.query.filter_by(ip=self.test_ip).first()
        self.assertIsNone(pdu)

    def test_remove_nonexistent_pdu(self):
        response = self.client.delete(url_for('pdu', ip='something'),
                                      headers=self.headers)
        self.assert_404(response)

    def test_update_pdu(self):
        self.create_test_pdu()

        new_hostname = 'new_hostname'
        new_pass = 'new_pass'

        data = json.dumps({'hostname': new_hostname,
                           'password': new_pass})

        response = self.client.put(url_for('pdu',
                                            ip=self.test_ip),
                                   headers=self.headers, data=data)
        self.assert_200(response)

        print response.json
        pdu = Pdu.query.filter_by(ip= self.test_ip).first()
        self.assertIsNotNone(pdu)
        self.assertEqual(new_hostname, pdu.hostname)
        self.assertEqual(new_pass, pdu.password)
