
Note : Snmpapi is desgined in similar fashion to IPMI api , If you have used ipmi api before you can replace user/users with snmpuser/snmpusers in url and machine/machines with pdu/pdus , while adding pdu just replace the fqdn with ip in details and everything will work as expected 

# Usage Examples

The flow below assumes a user `root` with a known password; this user cannot be deleted via the API.

## User Management

Login as `root` and get an authentication token. Future accesses can use this token instead
     of sending the username and password each time.

```
$ curl -i -u root:root -X GET http://localhost:5000/snmplogin

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 164
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 10:51:05 GMT

{
    "duration": 600, 
    "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzMjgxMDg2NSwiaWF0IjoxNDMyODEwMjY1fQ.eyJpZCI6MX0.kIou03_DewWFQap9wdlnf-FP-xaKz1GgPYw3UqMHlFk"
}

$ export TOKEN=eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzMjgxMDg2NSwiaWF0IjoxNDMyODEwMjY1fQ.eyJpZCI6MX0.kIou03_DewWFQap9wdlnf-FP-xaKz1GgPYw3UqMHlFk:unused
```

List the available users.

```
$ curl -i -u $TOKEN -X GET http://localhost:5000/snmpusers

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 499
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 10:52:56 GMT

{
    "users": [
        {
            "location": "http://localhost:5000/snmpusers/root", 
            "username": "root"
        }
    ]
}
```

Create user `igor` with password `igor`.

```
$ curl -i -u $TOKEN -X POST -H "Content-Type: application/json" -d '{"username":"igor", "password":"igor"}' http://localhost:5000/snmpusers

HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 84
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 10:54:45 GMT

{
    "location": "http://localhost:5000/snmpusers/igor", 
    "username": "igor"
}

```

Get an authentication token as user `igor`.

```
$ curl -i -u igor:igor -X GET http://localhost:5000/snmplogin

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 164
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 10:55:18 GMT

{
    "duration": 600, 
    "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzMjgxMTExOCwiaWF0IjoxNDMyODEwNTE4fQ.eyJpZCI6Mn0.dQZBC5EyZBmB7th92wYDdjvc3XF6kx590riNNXR5sk4"
}

$ export TOKEN=eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzMjgxMTExOCwiaWF0IjoxNDMyODEwNTE4fQ.eyJpZCI6Mn0.dQZBC5EyZBmB7th92wYDdjvc3XF6kx590riNNXR5sk4:unused
```

List the available users, that now contains `igor`.

```
$ curl -i -u $TOKEN -X GET http://localhost:5000/snmpusers

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 259
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 10:57:38 GMT

{
    "users": [
        {
            "location": "http://localhost:5000/snmpusers/root", 
            "username": "root"
        }, 
        {
            "location": "http://localhost:5000/snmpusers/igor", 
            "username": "igor"
        }
    ]
}
```

View details of the user `igor`.

```
$ curl -i -u $TOKEN -X GET http://localhost:5000/snmpusers/igor

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 84
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 10:58:08 GMT

{
    "location": "http://localhost:5000/snmpusers/igor", 
    "username": "igor"
}
```

Update the password for user `igor` (can only be done by `root` and `igor`).

```
$ curl -i -u $TOKEN -X PUT -H "Content-Type: application/json" -d '{"password": "password"}' http://localhost:5000/snmpusers/igor

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 49
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 10:58:39 GMT

{
    "message": "Updated entry for user igor"
}
```

Try obtaining a token with the old password for `igor`.

```
$ curl -i -u igor:igor -X GET http://localhost:5000/snmplogin
HTTP/1.0 401 UNAUTHORIZED
Content-Type: text/html; charset=utf-8
Content-Length: 19
WWW-Authenticate: Basic realm="Authentication Required"
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:00:28 GMT

Unauthorized Access

```

Try obtaining a token with the new password for `igor`.

```
$ curl -i -u igor:password -X GET http://localhost:5000/snmplogin

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 164
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:01:17 GMT

{
    "duration": 600, 
    "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzMjgxMTQ3NywiaWF0IjoxNDMyODEwODc3fQ.eyJpZCI6Mn0.5Ie0GQUwIQ-IJqO2yr9jBZNkxTdwwoZdMcLNhuv2Nv4"
}
```

Delete the user `igor` (can only be done by `root` and `igor`).

```
$ curl -i -u $TOKEN -X DELETE -H "Content-Type: application/json" http://localhost:5000/users/igor

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 39
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:02:12 GMT

{
    "message": "User igor deleted"
}

```

View the list of users as `root`.

```
$ curl -i -u root:root -X GET http://localhost:5000/users

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 141
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:02:37 GMT

{
    "users": [
        {
            "location": "http://localhost:5000/snmpusers/root", 
            "username": "root"
        }
    ]
}
```

## Pdu Management

The following examples assume the existence of a user `root` with password `root`,
and use username:password authentication instead of an auth token.

Add a new pdu.

```
$ curl -i -u root:root -X POST -H "Content-Type: application/json" -d '{"hostname": "osl01", "fqdn": "osl01.lab.osl.edu", "username":"osl", "password":"osl"}' http://localhost:5000/pdus


HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 143
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:07:06 GMT

{
    "ip": "10.0.0.10", 
    "location": "http://localhost:5000/pdus/10.0.0.10", 
    "users": "http://localhost:5000/pdus/10.0.0.10/users"
}

```

List available pdus.

```
$ curl -i -u root:root -X GET http://localhost:5000/pdus

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 207
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:07:45 GMT

{
    "pdus": [
        {
            "ip": "10.0.0.10", 
            "location": "http://localhost:5000/pdus/10.0.0.10", 
            "users": "http://localhost:5000/pdus/10.0.0.10/users"
        }
    ]
}
```

View pdu details.

```
$ curl -i -u root:root -X GET http://localhost:5000/pdus/10.0.0.10

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 169
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:08:29 GMT

{
    "hostname": "osl01", 
    "ip": "10.0.0.10", 
    "location": "http://localhost:5000/pdus/10.0.0.10", 
    "users": "http://localhost:5000/pdus/10.0.0.10/users"
}

```

Update pdu details.

```
$curl -i -u root:root -X PUT -H "Content-Type: application/json" -d '{"ip": "10.0.0.11", "username": "username", "password": "password"}' http://localhost:5000/pdus/10.0.0.10

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 53
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:11:15 GMT

{
    "message": "Updated entry for pdu 10.0.0.10"
}
```

Delete a pdu.

```
$curl -i -u root:root -X DELETE http://localhost:5000/pdus/10.0.0.10 

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 43
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:12:20 GMT

{
    "message": "Pdu 10.0.0.10 deleted"
}
```

## Permissions Management

Create a new pdu entry.

```
$curl -i -u root:root -X POST -H "Content-Type: application/json" -d '{"hostname": "osl01", "ip": "10.0.0.10", "username":"osl", "password":"osl"}' http://localhost:5000/pdus 

HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 143
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:13:53 GMT

{
    "ip": "10.0.0.10", 
    "location": "http://localhost:5000/pdus/10.0.0.10", 
    "users": "http://localhost:5000/pdus/10.0.0.10/users"
}
```

View pdus user `root` is permitted to access.

```
$ curl -i -X GET -u root:root http://localhost:5000/snmpusers/root/pdus

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 48
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:14:53 GMT

{
    "machines": [], 
    "username": "root"
}
```

View users having access to pdu `10.0.0.10`.

```
$ curl -i -X GET -u root:root http://localhost:5000/pdus/10.0.0.10/users

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 44
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:15:55 GMT

{
    "ip": "10.0.0.10", 
    "users": []
}
```

Add permission for user `root` to access pdu `10.0.0.10`.

```
$ curl -i -X PUT -u root:root http://localhost:5000/snmpusers/root/pdus/10.0.0.10

HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 71
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:16:53 GMT

{
    "message": "Created permission for user root to pdu 10.0.0.10"
}
```

View pdus user `root` is permitted to access.

```
$ curl -i -X GET -u root:root http://localhost:5000/snmpusers/root/pdus
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 168
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:17:47 GMT

{
    "machines": [
        {
            "ip": "10.0.0.10", 
            "location": "http://localhost:5000/pdus/10.0.0.10"
        }
    ], 
    "username": "root"
}
```

View users having access to pdu `10.0.0.10`.

```
$ curl -i -X GET -u root:root http://localhost:5000/pdus/10.0.0.10/users

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 165
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:18:57 GMT

{
    "ip": "10.0.0.10", 
    "users": [
        {
            "location": "http://localhost:5000/snmpusers/root", 
            "username": "root"
        }
    ]
}
```

Revoke permission for `root` to access `10.0.0.10`.

```
$ curl -i -X DELETE -u root:root http://localhost:5000/snmpusers/root/pdus/10.0.0.10

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 71
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:21:50 GMT

{
    "message": "Deleted permission for user root to pdu 10.0.0.10"
}
```

View pdus user `root` is permitted to access.

```
$ curl -i -X GET -u root:root http://localhost:5000/snmpusers/root/pdus

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 48
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:22:45 GMT

{
    "machines": [], 
    "username": "root"
}
```

View users having access to pdu `10.0.0.10`.

```
$ curl -i -X GET -u root:root http://localhost:5000/pdus/10.0.0.10/users

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 44
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:23:44 GMT

{
    "ip": "10.0.0.10", 
    "users": []
}
```

Add permission for user `root` to access pdu `10.0.0.10`.

```
$ curl -i -X PUT -u root:root http://localhost:5000/pdus/10.0.0.10/users/root

HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 71
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:24:45 GMT

{
    "message": "Created permission for user root to pdu 10.0.0.10"
}
```

View pdus user `root` is permitted to access.

```
$ curl -i -X GET -u root:root http://localhost:5000/snmpusers/root/pdus

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 168
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:25:36 GMT

{
    "machines": [
        {
            "ip": "10.0.0.10", 
            "location": "http://localhost:5000/pdus/10.0.0.10"
        }
    ], 
    "username": "root"
}
```

View users having access to pdu `10.0.0.10`.

```
$ curl -i -X GET -u root:root http://localhost:5000/pdus/10.0.0.10/users

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 165
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:26:34 GMT

{
    "ip": "10.0.0.10", 
    "users": [
        {
            "location": "http://localhost:5000/snmpusers/root", 
            "username": "root"
        }
    ]
}
```

Revoke permission for `root` to access pdu `10.0.0.10`.

```
$ curl -i -X DELETE -u root:root http://localhost:5000/pdus/10.0.0.10/users/root

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 71
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:29:37 GMT

{
    "message": "Deleted permission for user root to pdu 10.0.0.10"
}
```

View pdus user `root` is permitted to access.

```
$ curl -i -X GET -u root:root http://localhost:5000/snmpusers/root/pdus

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 44
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:30:40 GMT

{
    "pdus": [], 
    "username": "root"
}
```

View users having access to pdu `10.0.0.10`.

```
$ curl -i -X GET -u root:root http://localhost:5000/pdus/10.0.0.10/users

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 44
Server: Werkzeug/0.9.6 Python/2.7.9
Date: Thu, 28 May 2015 11:31:38 GMT

{
    "ip": "10.0.0.10", 
    "users": []
}
```

