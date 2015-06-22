#!/usr/bin/env python

import base64
import json
from flask import url_for

from . import IgorApiTestCase
from igor_rest_api.config import ROOT_USER, ROOT_PASS
from igor_rest_api.api.grouping.models import Group
from igor_rest_api.api.grouping.models import Useroutletsgroups
from igor_rest_api.api.grouping.models import Userdetails


class GroupingsPermissionsTestCase(IgorApiTestCase):

    test_userid = 1
    test_groupingid = 2
    test_pass = 'password'

    def setUp(self):
        # Login as ROOT_USER prior to all test cases
        super(GroupingsPermissionsTestCase, self).setUp()
        response = self.client.get(url_for('groupingslogin'),
                                   headers=[('Authorization', 'Basic '
                                             + base64.b64encode(ROOT_USER +
                                                                ':' +
                                                                ROOT_PASS))])
        self.headers = [('Authorization', 'Basic '
                         + base64.b64encode((response.json)['token']
                         + ':' + ROOT_USER)),
                        ('Content-Type', 'application/json')]

    def create_test_grouping(self, name='test_grouping'):
        group = Group(name)
        self.db.session.add(group)
        self.db.session.commit()
        return group

    def create_test_user(self, username='test_user'):
        user = Userdetails(username, self.test_pass)
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def test_list_user_groupings(self):
        user = self.create_test_user()

        response = self.client.get(url_for('groupings_user',
                                            id=user.id),
                                   headers=self.headers)
        self.assert_200(response)
        self.assertEquals(0, len((response.json)['username: '+user.username+' ']),
                          'no permissions should exist before grant')

        grouping1 = self.create_test_grouping(name='grouping_one')
        grouping2 = self.create_test_grouping(name='grouping_two')
        relation1 = Useroutletsgroups(user.id,grouping1.id)
        relation2 = Useroutletsgroups(user.id,grouping2.id)
        self.db.session.add(relation1)
        self.db.session.add(relation2)
        self.db.session.commit()


        response = self.client.get(url_for('groupings_user',
                                            id=user.id),
                                   headers=self.headers)
        self.assert_200(response)

        groupids = [group['groupid'] for group in
                    (response.json)['username: '+ user.username+ ' ']]

        self.assertIn(grouping1.id, groupids)
        self.assertIn(grouping2.id, groupids)
        self.assertEquals(2, len(groupids))

    def test_add_grouping_to_user(self):
        user = self.create_test_user()
        grouping = self.create_test_grouping()

        data = json.dumps({'outletgroupid': grouping.id,'userid': user.id})
        response = self.client.post(url_for('groupings_users'),
                                   data=data,
                                   headers=self.headers)
        self.assertStatus(response, 201)

        group = Useroutletsgroups.query.filter_by(userid=user.id).first()
        self.assertEquals(group.id, grouping.id,
                          'expected grouping to exist for user')


    def test_remove_machine_from_user(self):
        grouping = self.create_test_grouping()
        user = self.create_test_user()


        relation = Useroutletsgroups(user.id,grouping.id)
        self.db.session.add(relation)
        self.db.session.commit()
        data = json.dumps({'outletgroupid': grouping.id,'userid': user.id})

        response = self.client.delete(url_for('groupings_users'),
                                      data=data,
                                      headers=self.headers)
        print response.json
        self.assert_200(response, 'unexpected error deleting relation')

        relation = Useroutletsgroups.query.filter_by(userid=user.id,outletgroupid=grouping.id).first()
        self.assertEquals(None, relation)

