#!/usr/bin/env python

import base64
import json
from flask import url_for

from . import IgorApiTestCase
from igor_rest_api.config import ROOT_USER, ROOT_PASS
from igor_rest_api.api.grouping.models import Group

class GroupingsoutletgroupingsTestCase(IgorApiTestCase):

    test_groupname = 'groupname'
    test_outlets = 1

    def setUp(self):
        # Login as ROOT_USER prior to all test cases
        super(GroupingsoutletgroupingsTestCase, self).setUp()
        response = self.client.get(url_for('groupingslogin'),
                                   headers=[('Authorization', 'Basic '
                                             + base64.b64encode(ROOT_USER +
                                                                ':' +
                                                                ROOT_PASS))])
        self.headers = [('Authorization', 'Basic '
                         + base64.b64encode((response.json)['token']
                         + ':' + ROOT_USER)),
                        ('Content-Type', 'application/json')]

    def create_test_group(self):
        group = Group(self.test_groupname)
        self.db.session.add(group)
        self.db.session.commit()

    def test_list_groups(self):
        self.create_test_group()

        response = self.client.get(url_for('groupings_groups'), headers=self.headers)
        self.assert_200(response)

        grouping = (response.json)['groups'][0]
        self.assertEqual(self.test_groupname, grouping['name'],
                         'unexpected grouping name')

    def test_add_group(self):
        data = json.dumps({'name': self.test_groupname})

        response = self.client.post(url_for('groupings_groups'),
                                    data=data,
                                    headers=self.headers)
        self.assertStatus(response, 201)

        grouping = Group.query.filter_by(name=self.test_groupname).first()
        self.assertIsNotNone(grouping)
        self.assertEqual(self.test_groupname, grouping.name)


    def test_nonexistent_grouping_info(self):
        response = self.client.get(url_for('groupings_group', id=22627828),
                                   headers=self.headers)
        self.assert_404(response)


    def test_remove_nonexistent_grouping(self):
        response = self.client.delete(url_for('groupings_group', id=762728),
                                      headers=self.headers)
        self.assert_404(response)

    def test_update_grouping(self):
        self.create_test_group()

        new_name = 'new_name'

        data = json.dumps({'name': new_name})

        response = self.client.put(url_for('groupings_group',
                                            id=1),
                                   headers=self.headers, data=data)
        self.assert_200(response)

        print response.json
        group = Group.query.filter_by(id=1).first()
        self.assertIsNotNone(group)
        self.assertEqual(new_name, group.name)
