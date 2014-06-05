# Usage Examples

The flow below assumes a user `root` with a known password; this user cannot be deleted via the API.

## User Management

Login as `root` and get an authentication token. Future accesses can use this token instead
     of sending the username and password each time.

```
$ curl -i -u root:root -X GET http://localhost:5000/login
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 165
Server: Werkzeug/0.9.4 Python/2.7.6
Date: Mon, 02 Jun 2014 12:27:21 GMT

{
    "duration": 600, 
    "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQwMTcxMjY0MSwiaWF0IjoxNDAxNzEyMDQxfQ.eyJ1aWQiOjJ9.xrLAOK_OYBrWh7ZUzpuK7cuSkmk9Aak6pbleQR1-kpw"
}

$ export TOKEN=eyJhbGciOiJIUzI1NiIsImV4cCI6MTQwMTcxMjY0MSwiaWF0IjoxNDAxNzEyMDQxfQ.eyJ1aWQiOjJ9.xrLAOK_OYBrWh7ZUzpuK7cuSkmk:unused
```

List the available users.

```
$ curl -i -u $TOKEN -X GET http://localhost:5000/users
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 137
Server: Werkzeug/0.9.4 Python/2.7.6
Date: Mon, 02 Jun 2014 12:26:33 GMT

{
    "users": [
        {
            "location": "http://localhost:5000/users/root", 
            "username": "root"
        }
    ]
}
```

Create user `igor` with password `igor`.

```
$ curl -i -u $TOKEN -X POST -H "Content-Type: application/json" -d '{"username":"igor", "password":"igor"}' http://localhost:5000/users
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 80
Server: Werkzeug/0.9.4 Python/2.7.6
Date: Mon, 02 Jun 2014 12:29:45 GMT

{
    "location": "http://localhost:5000/users/igor", 
    "username": "igor"
}
```

Get an authentication token as user `igor`.

```
$ curl -i -u igor:igor -X GET http://localhost:5000/login
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 165
Server: Werkzeug/0.9.4 Python/2.7.6
Date: Mon, 02 Jun 2014 12:32:00 GMT

{
    "duration": 600, 
    "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQwMTcxMjkyMCwiaWF0IjoxNDAxNzEyMzIwfQ.eyJ1aWQiOjR9.5LtrccmtSD9hmBjqzd5vdFFeVJ3-KypdJcOgijdL2x8"
}


$ export TOKEN=eyJhbGciOiJIUzI1NiIsImV4cCI6MTQwMTcxMjkyMCwiaWF0IjoxNDAxNzEyMzIwfQ.eyJ1aWQiOjR9.5LtrccmtSD9hmBjqzd5vdFFeVJ3-KypdJcOgijdL2x8:unused
```

List the available users, that now contains `igor`.

```
$ curl -i -u $TOKEN -X GET http://localhost:5000/users
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 251
Server: Werkzeug/0.9.4 Python/2.7.6
Date: Mon, 02 Jun 2014 13:05:51 GMT

{
    "users": [
        {
            "location": "http://localhost:5000/users/root", 
            "username": "root"
        }, 
        {
            "location": "http://localhost:5000/users/igor", 
            "username": "igor"
        }
    ]
}
```

View details of the user `igor`.

```
$ curl -i -u $TOKEN -X GET http://localhost:5000/users/igor
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 80
Server: Werkzeug/0.9.4 Python/2.7.6
Date: Mon, 02 Jun 2014 13:06:26 GMT

{
    "location": "http://localhost:5000/users/igor", 
    "username": "igor"
}
```

Update the password for user `igor` (can only be done by `root` and `igor`).

```
$ curl -i -u $TOKEN -X PUT -H "Content-Type: application/json" -d '{"password": "password"}' http://localhost:5000/users/igor
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 49
Server: Werkzeug/0.9.4 Python/2.7.6
Date: Mon, 02 Jun 2014 13:13:36 GMT

{
    "message": "Updated entry for user igor"
}
```

Try obtaining a token with the old password for `igor`.

```
$ curl -i -u igor:igor -X GET http://localhost:5000/loginHTTP/1.0 401 UNAUTHORIZED
Content-Type: text/html; charset=utf-8
Content-Length: 19
WWW-Authenticate: Basic realm="Authentication Required"
Server: Werkzeug/0.9.4 Python/2.7.6
Date: Mon, 02 Jun 2014 13:14:00 GMT

Unauthorized Access
```

Try obtaining a token with the new password for `igor`.

```
$ curl -i -u igor:password -X GET http://localhost:5000/login
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 165
Server: Werkzeug/0.9.4 Python/2.7.6
Date: Mon, 02 Jun 2014 13:14:19 GMT

{
    "duration": 600, 
    "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQwMTcxNTQ1OSwiaWF0IjoxNDAxNzE0ODU5fQ.eyJ1aWQiOjR9.C43wlcG6cyUYztm7kn5wSmrl1QJq3y0bAQ2k8O6hma8"
}
```

Delete the user `igor` (can only be done by `root` and `igor`).

```
$ curl -i -u $TOKEN -X DELETE -H "Content-Type: application/json" http://localhost:5000/users/igor
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 39
Server: Werkzeug/0.9.4 Python/2.7.6
Date: Mon, 02 Jun 2014 13:14:50 GMT

{
    "message": "User igor deleted"
}
```

View the list of users as `root`.

```
$ curl -i -u root:root -X GET http://localhost:5000/users
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 137
Server: Werkzeug/0.9.4 Python/2.7.6
Date: Mon, 02 Jun 2014 13:15:15 GMT

{
    "users": [
        {
            "location": "http://localhost:5000/users/root", 
            "username": "root"
        }
    ]
}
```

## Machine Management

`TODO`

## IPMI Operations

`TODO`
