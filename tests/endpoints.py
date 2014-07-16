#!/usr/bin/env python

get_endpoints = ['user',
                 'users',
                 'machine',
                 'machines',
                 'user_machines',
                 'user_machine',
                 'machine_users',
                 'machine_user',
                 'machine_chassis',
                 'machine_chassis_power',
                 'machine_lan',
                 'machine_lan_channel'
                 ]

post_endpoints = ['users',
                  'machines',
                  'machine_chassis_power',
                  'machine_lan_channel'
                  ]

put_endpoints = ['user',
                 'machine',
                 'user_machine',
                 'machine_user',
                 ]

delete_endpoints = ['user',
                    'machine',
                    'user_machine',
                    'machine_user',
                    ]

all_endpoints = get_endpoints + \
                put_endpoints + \
                post_endpoints + \
                delete_endpoints
