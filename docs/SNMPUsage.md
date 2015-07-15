# API SUMMARY
```
/snmpusers                   GET => list , POST => create               
    /<username>              POST => update details, DELETE => delete
    
/pdus                        GET => list, POST => create
    /<ip>                    POST => edit, DELETE => delete
    
    /<ip>/<username>         PUT  => add user to pdu , DELETE => remove user from pdu
    
/pdu/<ip>/status              GET   => define a set of pdu info

/pdu/<ip>/status/<tower name>/<outlet id>    GET => return status of outlet, POST => change state of outlet  
```

# API Usage EXamples

## User Management
Login as `root` and get an authentication token. Future accesses can use this token instead of sending the username and password each time.
```
$ curl -i -u root:root -X GET http://localhost:5000/snmplogin
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 164
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 14 Jul 2015 07:10:58 GMT

{
    "duration": 600, 
    "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzNjg1ODQ1OCwiaWF0IjoxNDM2ODU3ODU4fQ.eyJpZCI6MX0.awgN3sHrCzQXkFT8FgEY9wL6zmmyEx7BM3N-H3FUM3Q"
}
```
$ export TOKEN=eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzMjgxMDg2NSwiaWF0IjoxNDMyODEwMjY1fQ.eyJpZCI6MX0.kIou03_DewWFQap9wdlnf-FP-xaKz1GgPYw3UqMHlFk:unused

List the available users.
```
$ curl -i -u $TOKEN -X GET http://localhost:5000/snmpusers
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 141
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 14 Jul 2015 07:12:57 GMT

{
    "users": [
        {
            "location": "http://localhost:5000/snmpusers/root", 
            "username": "root"
        }
    ]
}
```

Create user `igor` with password `igor`.(only root can add new users)
```
$ curl -i -u $TOKEN -X POST -H "Content-Type: application/json" -d '{"username":"igor", "password":"igor"}' http://localhost:5000/snmpusers
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 142
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 14 Jul 2015 07:13:42 GMT

{
    "location": "http://localhost:5000/snmpusers/igor", 
    "pdus": "http://localhost:5000/snmpusers/igor/pdus", 
    "username": "igor"
}
```

Get an authentication token as user `igor`.
```
$ curl -i -u igor:igor -X GET http://localhost:5000/snmplogin
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 164
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 14 Jul 2015 07:14:35 GMT

{
    "duration": 600, 
    "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzNjg1ODY3NSwiaWF0IjoxNDM2ODU4MDc1fQ.eyJpZCI6Mn0.jUWcofNXgI3YbsNfEpB6qu199DhIOx1BLFgxsyDkj3k"
}
```
use the auth token
```
export TOKEN=eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzNjg1ODY3NSwiaWF0IjoxNDM2ODU4MDc1fQ.eyJpZCI6Mn0.jUWcofNXgI3YbsNfEpB6qu199DhIOx1BLFgxsyDkj3k:unused
```

View details of the user `igor`.
```
$ curl -i -u $TOKEN -X GET http://localhost:5000/snmpusers/igor
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 142
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 14 Jul 2015 07:16:54 GMT

{
    "location": "http://localhost:5000/snmpusers/igor", 
    "pdus": "http://localhost:5000/snmpusers/igor/pdus", 
    "username": "igor"
}
```

Update the password for user `igor` (can only be done by `root` and `igor`).
```
$ curl -i -u $TOKEN -X PUT -H "Content-Type: application/json" -d '{"password": "password"}' http://localhost:5000/snmpusers/igor
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 49
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 14 Jul 2015 07:17:47 GMT

{
    "message": "Updated entry for user igor"
}
```

Delete the user `igor` (can only be done by `root` and `igor`).
```
$ curl -i -u igor:password -X DELETE -H "Content-Type: application/json" http://localhost:5000/snmpusers/igor
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 39
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 14 Jul 2015 07:23:36 GMT

{
    "message": "User igor deleted"
}
```

## Pdu Management

Add a new pdu.(only root can add new pdus)
```
$ curl -i -u root:root -X POST -H "Content-Type: application/json" -d '{"hostname": "osl01", "ip": "10.0.1.33","password":"osl"}' http://localhost:5000/pdus
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 143
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 14 Jul 2015 07:30:45 GMT

{
    "ip": "10.0.1.33", 
    "location": "http://localhost:5000/pdus/10.0.1.33", 
    "users": "http://localhost:5000/pdus/10.0.1.33/users"
}
```
List available pdus.
```
$ curl -i -u root:root -X GET http://localhost:5000/pdus
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 207
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 14 Jul 2015 07:31:28 GMT

{
    "pdus": [
        {
            "ip": "10.0.1.33", 
            "location": "http://localhost:5000/pdus/10.0.1.33", 
            "users": "http://localhost:5000/pdus/10.0.1.33/users"
        }
    ]
}
```
Update pdu details.(only root can do this)
```
$curl -i -u root:root -X PUT -H "Content-Type: application/json" -d '{"hostname": "new_hostname", "password": "password"}' http://localhost:5000/pdus/10.0.0.10
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 53
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 14 Jul 2015 07:32:47 GMT

{
    "message": "Updated entry for pdu 10.0.1.33"
}
```
Delete a pdu.(only root can do this)
```
$curl -i -u root:root -X DELETE http://localhost:5000/pdus/10.0.0.10
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 43
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 14 Jul 2015 07:33:46 GMT

{
    "message": "Pdu 10.0.1.33 deleted"
}
```

## Permissions Management

Create a new pdu entry.(root user has access to all the pdus)
```
$curl -i -u root:root -X POST -H "Content-Type: application/json" -d '{"hostname": "osl01", "ip": "10.0.1.33", "password":"osl"}' http://localhost:5000/pdus 
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 143
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 14 Jul 2015 08:06:47 GMT

{
    "ip": "10.0.1.33", 
    "location": "http://localhost:5000/pdus/10.0.1.33", 
    "users": "http://localhost:5000/pdus/10.0.1.33/users"
}
```
create user igor with password igor
```
curl -i -u root:root -X POST -H "Content-Type: application/json" -d '{"username":"igor", "password":"igor"}' http://localhost:5000/snmpusers
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 142
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 14 Jul 2015 08:08:12 GMT

{
    "location": "http://localhost:5000/snmpusers/igor", 
    "pdus": "http://localhost:5000/snmpusers/igor/pdus", 
    "username": "igor"
}
```
Add permission for user `igor` to access pdu `10.0.1.33`.
```
$ curl -i -X PUT -u root:root http://localhost:5000/snmpusers/igor/pdus/10.0.1.33
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 71
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 14 Jul 2015 08:09:43 GMT

{
    "message": "Created permission for user igor to pdu 10.0.1.33"
}
```
View pdus user `igor` is permitted to access.
```
$ curl -i -X GET -u root:root http://localhost:5000/snmpusers/igor/pdus
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 164
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 14 Jul 2015 08:10:46 GMT

{
    "pdus": [
        {
            "ip": "10.0.1.33", 
            "location": "http://localhost:5000/pdus/10.0.1.33"
        }
    ], 
    "username": "igor"
}
```
View users having access to pdu `10.0.1.33`.
```
$ curl -i -X GET -u root:root http://localhost:5000/pdus/10.0.1.33/users
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 165
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 14 Jul 2015 08:11:54 GMT

{
    "ip": "10.0.1.33", 
    "users": [
        {
            "location": "http://localhost:5000/snmpusers/igor", 
            "username": "igor"
        }
    ]
}
```
Revoke permission for `igor` to access pdu `10.0.1.33`.
```
$ curl -i -X DELETE -u root:root http://localhost:5000/pdus/10.0.1.33/users/igor
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 71
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 14 Jul 2015 08:13:51 GMT

{
    "message": "Deleted permission for user igor to pdu 10.0.1.33"
}
```

## PDU control 
To get status of all the outlets of pdu with ip '10.0.1.33'
```
$curl -i -u root:root -X GET http://localhost:5000/pdu/10.0.1.33/status
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 902
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 14 Jul 2015 08:26:56 GMT

{
    "amperage": {
        "tower_A": 63, 
        "tower_B": 88
    }, 
    "status": {
        "TowerA_Outlet1": "on", 
        "TowerA_Outlet2": "off", 
        "TowerA_Outlet3": "on", 
        "TowerA_Outlet4": "off", 
        "TowerA_Outlet5": "off", 
        "TowerA_Outlet6": "off", 
        "TowerA_Outlet7": "on", 
        "TowerA_Outlet8": "on", 
        "TowerB_Outlet1": "off", 
        "TowerB_Outlet10": "on", 
        "TowerB_Outlet11": "on", 
        "TowerB_Outlet12": "on", 
        "TowerB_Outlet13": "on", 
        "TowerB_Outlet14": "on", 
        "TowerB_Outlet15": "on", 
        "TowerB_Outlet16": "on", 
        "TowerB_Outlet2": "off", 
        "TowerB_Outlet3": "on", 
        "TowerB_Outlet4": "off", 
        "TowerB_Outlet5": "on", 
        "TowerB_Outlet6": "on", 
        "TowerB_Outlet7": "on", 
        "TowerB_Outlet8": "on", 
        "TowerB_Outlet9": "on"
    }
}

View status of specific outlet , for example to view status of Tower A ,outlet 3
```
$curl -i -u root:root -X GET http://localhost:5000/pdu/10.0.1.33/A/3
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 43
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Tue, 14 Jul 2015 08:29:29 GMT

{
    "amperage": 63, 
    "state": "on"
}
```
change state of outlet 3 in tower A
```
$curl -u root:root -H "Content-Type: application/json" -X POST -d '{"state":"off"}' http://localhost:5000/pdu/10.0.1.33/A/3
{
    "Success": "Changed state"
}
```
