# API SUMMARY 
```
/outlet_groups/users               GET => list, POST => create 
/outlet_groups/users/<id>/         POST => edit, DELETE => delete 
/outlet_groups/login               GET =>  return a auth token
/outlet_groups/pdu                 GET => list 
                  /<ip>/           POST => create, edit, DELETE => delete
/outlets                           GET => list, POST => create
        /<id>                      GET => details, POST => update, DELETE => delete
        /<id>/control              GET => details , POST {'action': <action(on,off,reboot> } => change state
/outlet_groups                      GET => list, POST => create
    /<id>/<outletid>                PUT,DELETE => edit (add/remove outlets via edit)
    /<id>/control                   POST {'action': <action>, 'value': <value>, ...} => status of action
    /<id>/query                     GET => defined set of info on outlets in group (voltage, load, etc)
    /<id>/users                     GET => list users
                                    POST {'username': <name>, ...} => add user to group
    /<id>/users/<user_id>    DELETE => remove user from group
```

# API Usage EXamples
## Pdu management
Only root can manage pdus
Create a new pdu entry  
```
$curl -i -u root:root -X POST -H "Content-Type: application/json" -d '{"ip": "10.0.1.37","access_string":"string","fqdn":"testfqdn"}' http://localhost:5000/outlet_groups/pdu
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 147
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Mon, 10 Aug 2015 09:24:23 GMT

{
    "location": "http://localhost:5000/outlet_groups/pdu/10.0.1.37", 
    "pdu_fqdn": "testfqdn", 
    "pdu_id": 2, 
    "pdu_ip": "10.0.1.37"
}
```
View all pdu's 
```
$curl -i -u root:root -X GET http://localhost:5000/outlet_groups/pdu

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 228
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Mon, 10 Aug 2015 09:25:15 GMT

{
    "pdus": [
        {
            "fqdn": "test", 
            "id": 1, 
            "ip": "10.0.1.33"
        }, 
        {
            "fqdn": "testfqdn", 
            "id": 2, 
            "ip": "10.0.1.37"
        }
    ]
}
```
View details of pdu with ip 10.0.1.33
```
$curl -i -u root:root  -X GET http://localhost:5000/outlet_groups/pdu/10.0.1.37

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 135
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Mon, 10 Aug 2015 09:26:06 GMT

{
    "Pdudetails": [
        {
            "fqdn": "testfqdn", 
            "id": 2, 
            "ip": "10.0.1.37"
        }
    ]
}
```
Modify access_string of pdu with ip 10.0.1.33
```
$curl -i -u root:root -X PUT -H "Content-Type: application/json" -d '{"access_string":"newstring"}' http://localhost:5000/outlet_groups/pdu/10.0.1.33
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 53
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 04:12:19 GMT

{
    "message": "Updated entry for pdu 10.0.1.33"
}
```
Delete pdu with ip 10.0.1.33
```
$curl -i -u root:root -X DELETE http://localhost:5000/outlet_groups/pdu/10.0.1.33
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 43
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 04:13:58 GMT

{
    "message": "Pdu 10.0.1.33 deleted"
}
```
Add a pdu for further testing 
```
$curl -i -u root:root -X POST -H "Content-Type: application/json" -d '{"ip": "10.0.1.33","access_string":"osl"}' http://localhost:5000/outlet_groups/pdu
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 118
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Thu, 16 Jul 2015 04:18:53 GMT

{
    "location": "http://localhost:5000/outlet_groups/pdu/10.0.1.33", 
    "pdu_id": 1, 
    "pdu_ip": "10.0.1.33"
}
```
## Outlet management
Add outlet of pdu with id 1 , tower A and oulet number 1 to be managed
```
$curl -i -u root:root -H "Content-Type: application/json" -X POST -d  '{"pduid":1,"towername":"A","outlet":1}' http://localhost:5000/outlets
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 106
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Thu, 16 Jul 2015 04:18:09 GMT

{
    "location": "http://localhost:5000/outlets/1", 
    "outlet_id": 1, 
    "outlet_ip": "10.0.1.33"
}
```
View all outlets
```
$curl -i -u root:root  -X GET http://localhost:5000/outlets
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 156
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 04:29:55 GMT

{
    "outlets": [
        {
            "id": 1, 
            "outlet": 1, 
            "pdu_ip": "10.0.1.33", 
            "tower": "A"
        }
    ]
}
```
View details of outlet with id 1
```
$curl -i -u root:root -X GET http://localhost:5000/outlets/1
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 155
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 04:31:57 GMT

{
    "outlet": [
        {
            "id": 1, 
            "outlet": 1, 
            "pdu_ip": "10.0.1.33", 
            "tower": "A"
        }
    ]
}
```
Change details of outlet with id 1
```
$curl -i -u root:root -H "Content-Type: application/json" -X POST -d '{"pduid":1,"towername":"B","outlet":8}' http://localhost:5000/outlets/1
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 48
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 04:32:43 GMT

{
    "message": "Updated entry for outlet 1"
}
```
Delete outlet with id 1
```
$curl -i -u root:root -X DELETE http://localhost:5000/outlets/1
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 46
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 04:33:55 GMT

{
    "message": "outlet with id 1 deleted"
}
```
Add two outlets 
```
$curl -i -u root:root -H "Content-Type: application/json" -X POST -d '{"pduid":1,"towername":"A","outlet":1}' http://localhost:5000/outlets
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 106
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Thu, 16 Jul 2015 04:19:47 GMT

{
    "location": "http://localhost:5000/outlets/1", 
    "outlet_id": 1, 
    "outlet_ip": "10.0.1.33"
}

$curl -i -u root:root -H "Content-Type: application/json" -X POST -d '{"pduid":1,"towername":"B","outlet":3}' http://localhost:5000/outlets
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 106
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Thu, 16 Jul 2015 04:20:15 GMT

{
    "location": "http://localhost:5000/outlets/2", 
    "outlet_id": 2, 
    "outlet_ip": "10.0.1.33"
}
```
## Group management
Only root can create and manage groups
Create new group with name group1
```
$curl -i -u root:root -H "Content-Type: application/json" -X POST -d '{"name":"group1"}' http://localhost:5000/outlet_groups
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 109
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Thu, 16 Jul 2015 04:22:36 GMT

{
    "group_id": 1, 
    "group_name": "group1", 
    "location": "http://localhost:5000/outlet_groups/1"
}
```
View all created groups
```
$curl -i -u root:root -X GET http://localhost:5000/outlet_groups
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 97
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 04:54:31 GMT

{
    "groups": [
        {
            "id": 1, 
            "name": "group1"
        }
    ]
}
```
View details of group with id 1
```
$curl -i -u root:root -X GET http://localhost:5000/outlet_groups/1
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 124
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 04:54:58 GMT

{
    "group": [
        {
            "id": 1, 
            "name": "group1", 
            "outlets": []
        }
    ]
}
```
Update name of group with id 1
```
$curl -i -u root:root -H "Content-Type: application/json" -X POST -d '{"name":"newname"}' http://localhost:5000/outlet_groups/1
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 47
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 04:55:34 GMT

{
    "message": "Updated entry for group 1"
}
```
Delete group with id 1
```
$curl -i -u root:root -X DELETE http://localhost:5000/outlet_groups/1
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 43
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 04:56:02 GMT

{
    "message": "group newname deleted"
}
```
Create new group
```
$curl -i -u root:root -H "Content-Type: application/json" -X POST -d '{"name":"group1"}' http://localhost:5000/outlet_groups
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 109
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Thu, 16 Jul 2015 04:34:57 GMT

{
    "group_id": 1, 
    "group_name": "group1", 
    "location": "http://localhost:5000/outlet_groups/1"
}
```
## Group-outlet management
Only root can add outlets to group
Add outlet with id 1 to group with id 1
```
$curl -i -u root:root  -X PUT http://localhost:5000/outlet_groups/1/1
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 43
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 05:03:33 GMT

{
    "Success": "added outlet to group"
}
```
To view details of group with id 1
```
$curl -i -u root:root -X GET http://localhost:5000/outlet_groups/1
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 255
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 05:04:08 GMT

{
    "group": [
        {
            "id": 1, 
            "name": "group1", 
            "outlets": [
                [
                    "10.0.1.33", 
                    "A", 
                    1
                ]
            ]
        }
    ]
}
```
To delete association between outlet_id 1 and group_id 1 from table
```
$curl -i -u root:root  -X DELETE  http://localhost:5000/outlet_groups/1/1
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 50
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 05:04:34 GMT

{
    "Success": "deleted outlet from grouping"
}
```
## User management
Only root can add new users
To add user named user1 with password testpass
```
$curl -i -u root:root -X POST -H "Content-Type: application/json" -d '{"username":"user1", "password":"testpass"}' http://localhost:5000/outlet_groups/users
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 92
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 05:05:42 GMT

{
    "location": "http://localhost:5000/outlet_groups/users/2", 
    "username": "user1"
}
```
To get a token for user user1 
```
$curl -i -u user1:testpass -X GET http://localhost:5000/outlet_groups/login
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 164
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 05:07:47 GMT

{
    "duration": 600, 
    "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzNjkzNzQ2NywiaWF0IjoxNDM2OTM2ODY3fQ.eyJpZCI6Mn0.nVfDPcrbqh9IVYTmni_UaN2NpOUngEsfykMDNxxxb1I"
}
```
To list all the users(both root and normal users can use this) 
```
$curl -i -u user1:testpass -X GET http://localhost:5000/outlet_groups/users
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 259
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 05:08:15 GMT

{
    "users": [
        {
            "location": "http://localhost:5000/outlet_groups/users/1", 
            "userid": 1,
            "username": "root"
        }, 
        {
            "location": "http://localhost:5000/outlet_groups/users/2", 
            "userid": 2,
            "username": "user1"
        }
    ]
}
```
To change password of user (both root and user can passwords)
```
$curl -i -u user1:testpass -X POST -H "Content-Type: application/json" -d '{ "password":"pass"}' http://localhost:5000/outlet_groups/users/2
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 46
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 05:08:45 GMT

{
    "message": "Updated entry for user 2"
}
```
To delete user1 (both user1 and root can do this)
```
$curl -i -u root:root -X DELETE http://localhost:5000/outlet_groups/users/2
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 40
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 05:09:13 GMT

{
    "message": "User user1 deleted"
}
```
Create a new user
``` 
$curl -i -u root:root -X POST -H "Content-Type: application/json" -d '{"username":"user1", "password":"testpass"}' http://localhost:5000/outlet_groups/users
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 92
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 05:09:51 GMT

{
    "location": "http://localhost:5000/outlet_groups/users/2", 
    "username": "user1"
}
```
Add give user1 the permission to control group1
```
$curl -i -u root:root -X POST -H "Content-Type: application/json" -d '{"outletgroupid":1, "userid":2}' http://localhost:5000/outlet_groups/user/groups
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 150
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 05:11:24 GMT

{
    "grouping": "http://localhost:5000/outlet_groups/1", 
    "location": "http://localhost:5000/outlet_groups/users/2", 
    "username": "user1"
}
```
To view all the relations between user and groups
```
$curl -i -u root:root -X GET http://localhost:5000/outlet_groups/user/groups
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 106
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 05:13:30 GMT

{
    "relations": [
        {
            "outletgroupid": 1, 
            "userid": 2
        }
    ]
}
```
To delete relation between user1 and group1
```
$curl -i -u root:root -X DELETE -H "Content-Type: application/json" -d '{"outletgroupid":1, "userid":2}' http://localhost:5000/outlet_groups/user/groups
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 76
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 05:13:59 GMT

{
    "message": "Relation between Userid 2 and outletgroup 1 is deleted"
}
```
## controlling state of outletgrouping

root user can control all the outlet groupings and individual outlets, normal user can control the outletgroupings associated with him , and individual outlets 
which are present in groupings associated with him

To switch off all the outlets belonging to outletgrouping with id 1
```
$curl -i -u root:root -H "Content-Type: application/json" -X POST -d '{"action":"off"}' http://localhost:5000/outlet_groups/1/control
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 110
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 05:24:18 GMT

{
    "Status": {
        "10.0.1.33 A 1": "changed state", 
        "10.0.1.33 B 3": "changed state"
    }
}
```
To get status of all the outlets belonging to groupid 1
```
$ curl -i -u root:root  -X GET http://localhost:5000/outlet_groups/1/control
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 175
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 05:24:57 GMT

{
    "Status": {
        "10.0.1.33 A 1": "off", 
        "10.0.1.33 B 3": "off"
    }, 
    "amperages": {
        "10.0.1.33 A 1": 63, 
        "10.0.1.33 B 3": 75
    }
}
```
individual outlets can also be controlled using the api,to switch on outlet with id 1
```
$curl -i -u root:root -H "Content-Type: application/json" -X POST -d '{"action":"on"}' http://localhost:5000/outlet/1/control
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 67
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 05:25:44 GMT

{
    "Status": {
        "10.0.1.33 A 1": "changed state"
    }
}
```
To get status of outlet with id 1
```
$curl -i -u root:root -X GET http://localhost:5000/outlet/1/control
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 81
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 15 Jul 2015 05:26:26 GMT

{
    "Status": {
        "10.0.1.33 A 1": "on", 
        "amperage": 63
    }
}
```
