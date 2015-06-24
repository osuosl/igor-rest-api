
# Usage Examples

## Pdu management
Only root can manage pdus
Create a new pdu entry  
```
$ curl -i -u root:root -X POST -H "Content-Type: application/json" -d '{"ip": "10.10.10.11","access_string":"string"}' http://localhost:5000/groupings/pdu

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 31
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 10 Jun 2015 10:27:22 GMT

{
    "Success": "added pdu 10.10.10.11"
}
```

View all pdu's 
```
$curl -i -u root:root -X GET http://localhost:5000/groupings/pdu


{
    "pdus": [
        {
            "id": 1, 
            "ip": "10.10.10.11"
        }
    ]
}
```
View details of pdu with ip 10.10.10.11
```
$curl -i -u root:root  -X GET http://localhost:5000/groupings/pdu/10.10.10.11

{
    "Pdudetails": [
        {
            "id": 3, 
            "ip": "10.10.10.11"
        }
    ]
}

```
Modify access_string of pdu with ip 10.10.10.11
```
$curl -i -u root:root -X PUT -H "Content-Type: application/json" -d '{"access_string":"newstring"}' http://localhost:5000/groupings/pdu/10.10.10.11

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 55
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 10 Jun 2015 10:30:03 GMT

{
    "message": "Updated entry for pdu 10.10.10.11"
}
```

Delete pdu with ip 10.10.10.11
```
$curl -i -u root:root -X DELETE http://localhost:5000/groupings/pdu/10.10.10.11

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 45
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 10 Jun 2015 10:31:59 GMT

{
    "message": "Pdu 10.10.10.11 deleted"
}
```
Now the pdu entries will be empty
```
$curl   -X GET http://localhost:5000/groupings/pdu

{
    "pdus": []
}
```

Add two pdu's 
```
$curl -i -u root:root -X POST -H "Content-Type: application/json" -d '{"ip": "10.10.10.11","access_string":"string"}' http://localhost:5000/groupings/pdu

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 31
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 10 Jun 2015 10:32:31 GMT

{
    "Success": "added pdu 10.10.10.11"
}

$curl -i -u root:root -X POST -H "Content-Type: application/json" -d '{"ip": "10.10.10.21","access_string":"string"}' http://localhost:5000/groupings/pdu

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 31
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 10 Jun 2015 10:32:54 GMT

{
    "Success": "added pdu 10.10.10.21"
}
```

## Outlet management
Only root can manage outlets
Add outlet of pdu with id 1 , tower A and oulet number 1 to be managed
```
$curl -i -u root:root -H "Content-Type: application/json" -X POST -d '{"pduid":1,"towername":"A","outlet":1}' http://localhost:5000/groupings/outlets

{
    "Success": "added outlet"
}
```

View all outlets
```
$curl -i -u root:root  -X GET http://localhost:5000/groupings/outlets

{
    "outlets": [
        {
            "id": 1, 
            "outlet": 1, 
            "pdu_ip": "10.10.10.11", 
            "tower": "A"
        }
    ]
}
```

View details of outlet with id 1
```
$curl -i -u root:root -X GET http://localhost:5000/groupings/outlets/1

{
    "outlets": [
        {
            "id": 1, 
            "outlet": 8, 
            "pdu_ip": "10.10.10.11", 
            "tower": "B"
        }
    ]
}
```

Change details of outlet with id 1
```
$curl -i -u root:root -H "Content-Type: application/json" -X PUT -d '{"pduid":2,"towername":"B","outlet":8}' http://localhost:5000/groupings/outlets/1

{
    "message": "Updated entry for outlet 1"
}
```

Delete outlet with id 1
```
$curl -i -u root:root -X DELETE http://localhost:5000/groupings/outlets/1

{
    "message": "outlet with id 1 deleted"
}
```

Add two outlets
```
$curl -i -u root:root -H "Content-Type: application/json" -X POST -d '{"pduid":2,"towername":"A","outlet":1}' http://localhost:5000/groupings/outlets

{
    "Success": "added outlet"
}

$curl -i -u root:root -H "Content-Type: application/json" -X POST -d '{"pduid":1,"towername":"B","outlet":3}' http://localhost:5000/groupings/outlets

{
    "Success": "added outlet"
}
```

## Group management
Only root can create and manage groups
Create new group with name group1
```
$curl -i -u root:root -H "Content-Type: application/json" -X POST -d '{"name":"group1"}' http://localhost:5000/groupings/groups

{
    "Success": "added group group1"
}
```

View all created groups
```
$curl -i -u root:root -X GET http://localhost:5000/groupings/groups

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
$curl -i -u root:root -X GET http://localhost:5000/groupings/groups/1

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 124
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Fri, 12 Jun 2015 04:14:37 GMT

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
$curl -i -u root:root -H "Content-Type: application/json" -X PUT -d '{"name":"newname"}' http://localhost:5000/groupings/groups/1

{
    "message": "Updated entry for group 1"
}
```

Delete group with id 1
```
$curl -i -u root:root -X DELETE http://localhost:5000/groupings/groups/1

{
    "message": "group newname deleted"
}
```

Create new group
```
$curl -i -u root:root -H "Content-Type: application/json" -X POST -d '{"name":"group1"}' http://localhost:5000/groupings/groups

{
    "Success": "added group group1"
}
```

## Group-outlet management
Only root can add outlets to group
Add outlet with id 1 to group with id 1
```
$curl -i -u root:root -H "Content-Type: application/json" -X POST -d '{"outlet_id":1,"group_id":1}' http://localhost:5000/groupings/groupings

{
    "Success": "added outlet to group"
}
```

To view all the group id's and associated outlet id's
```
$curl -i -u root:root -X GET http://localhost:5000/groupings/groupings

{
    "groupoutlets": [
        {
            "group_id": 1, 
            "outlet_id": 1
        }
    ]
}
```
To view details of group with id 1
```
$curl -i -u root:root -X GET http://localhost:5000/groupings/groups/1
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 257
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Fri, 12 Jun 2015 04:26:01 GMT

{
    "group": [
        {
            "id": 1, 
            "name": "group1", 
            "outlets": [
                [
                    "10.10.10.21", 
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
$curl -i -u root:root -H "Content-Type: application/json" -X DELETE -d '{"outlet_id":1,"group_id":1}' http://localhost:5000/groupings/groupings

{
    "Success": "deleted grouping"
}
```

## User management
Only root can add new users
To add user named user1 with password testpass
```
$curl -i -u root:root -X POST -H "Content-Type: application/json" -d '{"username":"user1", "password":"testpass"}' http://localhost:5000/groupings/users

HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 92
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Fri, 12 Jun 2015 04:49:20 GMT

{
    "location": "http://localhost:5000/groupings/users/user1", 
    "username": "user1"
}
```

To get a token for user user1 
```
$curl -i -u user1:testpass -X GET http://localhost:5000/groupings/login

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 164
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Fri, 12 Jun 2015 04:57:13 GMT

{
    "duration": 600, 
    "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzNDA4NTYzMywiaWF0IjoxNDM0MDg1MDMzfQ.eyJpZCI6Mn0.m7mU2Oi_tg8hSilGadStuhPHreCHqCrYBeiPEVic8ls"
}
```

To list all the users(both root and normal users can use this) 
```
$curl -i -u user1:testpass -X GET http://localhost:5000/groupings/users

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 273
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Fri, 12 Jun 2015 04:50:18 GMT

{
    "users": [
        {
            "location": "http://localhost:5000/groupings/users/root", 
            "username": "root"
        }, 
        {
            "location": "http://localhost:5000/groupings/users/user1", 
            "username": "user1"
        }
    ]
}
```

To change password of user (both root and user can passwords)
```
$curl -i -u user1:testpass -X PUT -H "Content-Type: application/json" -d '{ "password":"pass"}' http://localhost:5000/groupings/users/user1

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 50
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Fri, 12 Jun 2015 04:52:36 GMT

{
    "message": "Updated entry for user user1"
}
```

To delete user1 (both user1 and root can do this)
```
$curl -i -u user1:pass -X DELETE http://localhost:5000/groupings/users/user1

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 40
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Fri, 12 Jun 2015 04:54:42 GMT

{
    "message": "User user1 deleted"
}
```

Create a new user
``` 
$curl -i -u root:root -X POST -H "Content-Type: application/json" -d '{"username":"user1", "password":"testpass"}' http://localhost:5000/groupings/users

HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 92
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Fri, 12 Jun 2015 04:55:20 GMT

{
    "location": "http://localhost:5000/groupings/users/user1", 
    "username": "user1"
}
```

Add give user1 the permission to control group1
```
$curl -i -u root:root -X POST -H "Content-Type: application/json" -d '{"outletgroupid":1, "userid":2}' http://localhost:5000/groupings/user/groups

HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 154
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Fri, 12 Jun 2015 05:10:01 GMT

{
    "grouping": "http://localhost:5000/groupings/groups/1", 
    "location": "http://localhost:5000/groupings/users/user1", 
    "username": "user1"
}
```
To view all the relations between user and groups
```
$curl -i -u root:root -X GET http://localhost:5000/groupings/user/groups

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 106
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Fri, 12 Jun 2015 05:12:17 GMT

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
$curl -i -u root:root -X DELETE -H "Content-Type: application/json" -d '{"outletgroupid":1, "userid":2}' http://localhost:5000/groupings/user/groups

HTTP/1.0 400 BAD REQUEST
Content-Type: application/json
Content-Length: 76
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Fri, 12 Jun 2015 05:13:10 GMT

{
    "message": "Relation between Userid 2 and outletgroup 1 is deleted"
}
```

## controlling state of outletgrouping

root user can control all the outlet groupings and individual outlets, normal user can control the outletgroupings associated with him , and individual outlets 
which are present in groupings associated with him

To switch off all the outlets belonging to outletgrouping with id 1
```
$curl -i -u root:root -H "Content-Type: application/json" -X POST -d '{"action":"off"}' http://localhost:5000/group/1

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 110
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 16 Jun 2015 16:01:45 GMT

{
    "Status": {
        "10.0.1.33 A 1": "chnaged state", 
        "10.0.1.33 B 2": "chnaged state"
    }
}
```

To get status of all the outlets belonging to groupid 1

```
$ curl -i -u user1:testpass  -X GET http://localhost:5000/group/1

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 90
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 16 Jun 2015 16:04:16 GMT

{
    "Status": {
        "10.0.1.33 A 1": "off", 
        "10.0.1.33 B 2": "off"
    }
}
```
individual outlets can also be controlled using the api,to switch on outlet with id 1
```
$curl -i -u user1:testpass -H "Content-Type: application/json" -X POST -d '{"action":"on"}' http://localhost:5000/outlet/1

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 67
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 16 Jun 2015 16:05:49 GMT

{
    "Status": {
        "10.0.1.33 A 1": "chnaged state"
    }
}
```

To get status of outlet with id 1
```
$curl -i -u root:root -X GET http://localhost:5000/outlet/1

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 56
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 16 Jun 2015 16:06:38 GMT

{
    "Status": {
        "10.0.1.33 A 1": "on"
    }
}
```
