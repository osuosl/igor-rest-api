
# Usage Examples

## Pdu management
Create a new pdu entry 
```
$ curl -i -X POST -H "Content-Type: application/json" -d '{"ip": "10.10.10.11","access_string":"string"}' http://localhost:5000/groupings/pdu

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 31
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 10 Jun 2015 10:27:22 GMT

{
    "Success": "added pdu"
}
```

View all pdu's
```
$curl -X GET http://localhost:5000/groupings/pdu


{
    "pdus": [
        {
            "id": 1, 
            "ip": "10.10.10.11"
        }
    ]
}
```
View details of pdu with id 1
```
$curl   -X GET http://localhost:5000/groupings/pdu/10.10.10.11

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
$curl -i -X PUT -H "Content-Type: application/json" -d '{"access_string":"newstring"}' http://localhost:5000/groupings/pdu/10.10.10.11

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
$curl -i -X DELETE http://localhost:5000/groupings/pdu/10.10.10.11

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
$curl -i -X POST -H "Content-Type: application/json" -d '{"ip": "10.10.10.11","access_string":"string"}' http://localhost:5000/groupings/pdu

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 31
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 10 Jun 2015 10:32:31 GMT

{
    "Success": "added pdu"
}

$curl -i -X POST -H "Content-Type: application/json" -d '{"ip": "10.10.10.21","access_string":"string"}' http://localhost:5000/groupings/pdu

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 31
Server: Werkzeug/0.9.6 Python/2.7.10
Date: Wed, 10 Jun 2015 10:32:54 GMT

{
    "Success": "added pdu"
}
```

## Outlet management
Add outlet of pdu with id 1 , tower A and oulet number 1 to be managed
```
$curl  -H "Content-Type: application/json" -X POST -d '{"pduid":1,"towername":"A","outlet":1}' http://localhost:5000/groupings/outlets

{
    "Success": "added outlet"
}
```

View all outlets
```
$curl   -X GET http://localhost:5000/groupings/outlets

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
$curl -X GET http://localhost:5000/groupings/outlets/1

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
$curl  -H "Content-Type: application/json" -X PUT -d '{"pduid":2,"towername":"B","outlet":8}' http://localhost:5000/groupings/outlets/1

{
    "message": "Updated entry for outlet 1"
}
```

Delete outlet with id 1
```
$curl   -X DELETE http://localhost:5000/groupings/outlets/1

{
    "message": "outlet with id 1 deleted"
}
```

Add two outlets
```
$curl  -H "Content-Type: application/json" -X POST -d '{"pduid":2,"towername":"A","outlet":1}' http://localhost:5000/groupings/outlets

{
    "Success": "added outlet"
}

$curl  -H "Content-Type: application/json" -X POST -d '{"pduid":3,"towername":"B","outlet":3}' http://localhost:5000/groupings/outlets

{
    "Success": "added outlet"
}
```

## Group management

Create new group with name group1
```
$curl  -H "Content-Type: application/json" -X POST -d '{"name":"group1"}' http://localhost:5000/groupings/groups

{
    "Success": "added group"
}
```

View all created groups
```
$curl   -X GET http://localhost:5000/groupings/groups

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
$curl   -X GET http://localhost:5000/groupings/groups/1

{
    "group": [
        {
            "id": 1, 
            "name": "group1"
        }
    ]
}
```

Update name of group with id 1
```
$curl  -H "Content-Type: application/json" -X PUT -d '{"name":"newname"}' http://localhost:5000/groupings/groups/1

{
    "message": "Updated entry for group 1"
}
```

Delete group with id 1
```
$curl  -X DELETE http://localhost:5000/groupings/groups/1

{
    "message": "group newname deleted"
}
```

Create new group
```
$curl  -H "Content-Type: application/json" -X POST -d '{"name":"group1"}' http://localhost:5000/groupings/groups

{
    "Success": "added group"
}
```

## Group-outlet management

Add outlet with id 1 to group with id 1
```
$curl  -H "Content-Type: application/json" -X POST -d '{"outlet_id":1,"group_id":1}' http://localhost:5000/groupings/groupings

{
    "Success": "added outlet to group"
}
```

To view all the group id's and associated outlet id's
```
$curl   -X GET http://localhost:5000/groupings/groupings

{
    "groupoutlets": [
        {
            "group_id": 1, 
            "outlet_id": 1
        }
    ]
}
```

To delete outlet_id 1 and group_id 1 from table
```
$curl  -H "Content-Type: application/json" -X DELETE -d '{"outlet_id":1,"group_id":1}' http://localhost:5000/groupings/groupings

{
    "Success": "deleted grouping"
}
```
