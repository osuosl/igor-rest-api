
# REST API Design

## Goals

The Api should give endpoints to manage individual Pdus, create logical groupings of pdu outlets and provide endpoints to manage them.
User should be able to perform operations like turn off, turn on, reboot and get amperage details from pdus and outlet groupings

### User Management

   * Root user will be created during database initialization and can't be deleted and he will have access to all the operations
   * Root user can add users and users can be associated with Pdus and outlet groupings
   * Users can generate access tokens and can use them as login credentials

### Pdu and outlet groupings management

   * Each pdu will have a access string , ip and fqdn associated with it
   * Various pdu outlets can be grouped together using the api
   * Once a user is associated with pdu or outlet grouping he can perform operations like turn on, turn off and reboot 
   * User associated with pdus and outlet groupings can also get amperage readings using the Api


## Interface

All operations will be implemented via HTTP verbs on URLS

Users will be authenticated using basic auth 

Data in post requests shoud be sent using json form , Api will return responses in json form

### Api Endpoints

`/pdu`

   * `GET` : will return the list of pdus

   ```
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

   * `POST` : will add new pdu to api database

   ```
    {
    "ip": "10.0.1.37",
    "access_string":"string",
    "fqdn":"testfqdn"
    }
   ```

`/pdu/<pdu_ip>`

   * `GET` : will return the details of pdu with specified ip

   ```
{
    "Pdudetails": [
        {
            "fqdn": "testfqdn", 
            "id": 2, 
            "ip": "10.0.1.37",
            "users": []
        }
    ]
}

   ```
   * `DELETE` : will delete the pdu from api database

   ```
{
    "message": "Pdu 10.0.1.33 deleted"
}
   ```

   * `PUT` : can be used to modify the access_string and ip address of pdu

   ```
    {
    "access_string":"newstring"
    }
   ```

`/pdu/<pdu_ip>/<user_id>`

   * `PUT` : will associate user with specified user_id to pdu with pdu_ip and he can control pdu outlets

   ```
    {
        "Success": "added user to pdu"
    }
   ```

   * `DELETE` : will delete the association between user and pdu

   ```
    {
        "Success": "deleted user from pdu"
    }
   ```


`/outlets`

   * `GET` : will return the list of outlets which are being managed

   ```
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

   * `POST` : will create a new outlet entry in database

   ```
    {
        "pduid":1,
        "towername":"A",
        "outlet":1
    }
   ```


`/outlets/<outlet_id>`

   * `GET` : will return the details of outlet with specified id

    ```
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

   * `POST` : this can be used to modify the details of outlet

    ```
    {
        "pduid":1,
        "towername":"B",
        "outlet":8
    }
    ```

   * `DELETE` : will delete the outlet from list of outlets to be managed

    ```
    {
        "message": "outlet with id 1 deleted"
    }
    ```

`/outlet_groups`


   * `GET` : will return the list of all the outlet groupings 

   ```

    {
        "groups": [
            {
                "id": 1, 
                "name": "group1"
            }
        ]
    }
   ```


   * `POST` : will create a new outlet grouping with specified name

   ```
    {       
        "name":"group1"
    }
   ```

`/outlet_groups/<id>`

   * `GET` : will return the details of specified outlet grouping

   ```
    {
        "group": [
            {
                "id": 1, 
                "name": "group1", 
                "outlets": [],
                "users": []
            }
        ]
    }
   ```

   * `POST` : this can be used to modify the name of outlet grouping

   ```
    {       
        "name":"group1"
    }
   ```

   * `DELETE` : this will delete the outlet grouping from database

   ```
    {
        "message": "group group1 deleted"
    }
   ```

`/outlet_groups/<id>/<outletid>`

   * `PUT` : will add the outlet with id as outletid to outlet grouping with specified id

   ```
    {
        "Success": "added outlet to group"
    }
   ```

   * `DELETE` : will remove the outlet from list of outlets belonging to outlet grouping

   ```
    {
        "Success": "deleted outlet from grouping"
    }
   ```

`/outlet_groups/users/groups`

   * `POST` : will add the user specified in post data to outlet grouping specified in post data

   ```
    {
        "outletgroupid":1,
        "userid":2
    }
   ```

   * `DELETE` : will delete the association between user and outlet grouping as specified in json data request

   ```
    {
        "outletgroupid":1,
        "userid":2
    }
   ```

`/outlet_groups/users`

   * `GET` : will return the list of users along with their userids

   ```
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

   * `POST` : will create a new user with specified username and password

   ```
    {
        "username":"user1",
        "password":"testpass"
    }
  ```


`/outlet_groups/users/<user_id>`

   * `POST` : this can be used to update the password of user 

   ```
    { 
        "password":"pass"
    }
   ```

   * `DELETE` : will delete the user with user_id from database

   ```
    {
        "message": "User user1 deleted"
    }
   ```

`/pdu/<pdu_ip>/control`

   * `GET` : will return the amperage and status of all the outlets of specified pdu

   ```
    {
        "amperage": {
            "tower_A": 63, 
            "tower_B": 88
        }, 
        "status": {
            "TowerA_Outlet1": "off", 
            "TowerA_Outlet2": "on", 
            "TowerA_Outlet3": "off", 
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
   ```

`/pdu/<pdu_ip>/<tower>/<outlet>/control`

   * `GET` : will return the amperage and state of specified outlet 

   ```
    {
        "amperage": 88, 
        "state": "off"
    }
   ```

   * `POST` : this can be used to change the status of specified outlet

   ```
    {
        "action":"on"
    }
   ```

`/outlet_groups/<id>/control`

   * `POST` : this can be used to change the status of specified outlet grouping

   ```
    {
        "action":"off"
    }
   ```

   * `GET` : this can be used to get the status and amperages of all the outlets present in outlet grouping

   ```
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


`/outlet/<id>/control`

   * `POST` : this can be used to control the outlet with specified outlet id

   ```
    {
        "action":"off"
    }
   ```

   * `GET` : will return the amperage and status of outlet with specified outlet id

   ```
    {
        "Status": {
            "10.0.1.33 A 1": "on", 
            "amperage": 63
        }
    }
   ```
