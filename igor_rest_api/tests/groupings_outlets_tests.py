#!/usr/bin/env python

import base64
import json
from flask import url_for

from . import IgorApiTestCase
from igor_rest_api.config import ROOT_USER, ROOT_PASS
from igor_rest_api.api.grouping.models import Outlets

class GroupingsoutletsTestCase(IgorApiTestCase):

    test_pduid = 1
    test_tower = 'test_tower'
    test_outlet = 1

    def setUp(self):
        # Login as ROOT_USER prior to all test cases
        super(GroupingsoutletsTestCase, self).setUp()
        response = self.client.get(url_for('groupingslogin'),
                                   headers=[('Authorization', 'Basic '
                                             + base64.b64encode(ROOT_USER +
                                                                ':' +
                                                                ROOT_PASS))])
        self.headers = [('Authorization', 'Basic '
                         + base64.b64encode((response.json)['token']
                         + ':' + ROOT_USER)),
                        ('Content-Type', 'application/json')]

    def create_test_outlet(self):
        outlet = Outlets(self.test_pduid, self.test_tower,self.test_outlet)
        self.db.session.add(outlet)
        self.db.session.commit()

    def test_list_outlets(self):
        self.create_test_outlet()

        response = self.client.get(url_for('groupings_outlets'), headers=self.headers)
        self.assert_200(response)

        outlet = (response.json)['outlets'][0]
        self.assertEqual(self.test_tower, outlet['tower'],
                         'unexpected pdu tower')
        self.assertEqual(self.test_outlet, outlet['outlet'],
                         'unexpected pdu outlet')

    def test_add_outlet(self):
        data = json.dumps({'pduid': self.test_pduid,
                            'towername': self.test_tower,
                            'outlet': self.test_outlet})

        response = self.client.post(url_for('groupings_outlets'),
                                    data=data,
                                    headers=self.headers)
        self.assertStatus(response, 201)

        outlet = Outlets.query.filter_by(pdu_id=self.test_pduid).first()
        self.assertIsNotNone(outlet)
        self.assertEqual(self.test_tower, outlet.towername)
        self.assertEqual(self.test_outlet, outlet.outlet)


    def test_nonexistent_outlet_info(self):
        response = self.client.get(url_for('groupings_outlet', id=22627828),
                                   headers=self.headers)
        self.assert_404(response)


    def test_remove_nonexistent_outlet(self):
        response = self.client.delete(url_for('groupings_outlet', id=762728),
                                      headers=self.headers)
        self.assert_404(response)

    def test_update_outlet(self):
        self.create_test_outlet()

        new_tower = 'new_tower'

        data = json.dumps({'towername': new_tower})

        response = self.client.put(url_for('groupings_outlet',
                                            id=1),
                                   headers=self.headers, data=data)
        self.assert_200(response)

        print response.json
        outlet = Outlets.query.filter_by(id=1).first()
        self.assertIsNotNone(outlet)
        self.assertEqual(new_tower, outlet.towername)
