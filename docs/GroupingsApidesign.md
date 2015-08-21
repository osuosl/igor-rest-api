
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

   * `GET` 

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

   * `POST`

   ```
    {
    "ip": "10.0.1.37",
    "access_string":"string",
    "fqdn":"testfqdn"
    }
   ```

`/pdu/<pdu_ip>`

   * `GET`

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
   * `DELETE` 

   ```
{
    "message": "Pdu 10.0.1.33 deleted"
}
   ```

   * `PUT`

   ```
    {
    "access_string":"newstring"
    }
   ```

`/pdu/<pdu_ip><user_id>`

   * `PUT` 

   ```
    {
        "Success": "added user to pdu"
    }
   ```

   * `DELETE`

   ```
    {
        "Success": "deleted user from pdu"
    }
   ```


`/outlets`

   * `GET`

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

   * `POST`

   ```
    {
        "pduid":1,
        "towername":"A",
        "outlet":1
    }
   ```


`/outlets/<outlet_id>`

   * `GET`

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

   * `POST`

    ```
    {
        "pduid":1,
        "towername":"B",
        "outlet":8
    }
    ```

   * `DELETE`

    ```
    {
        "message": "outlet with id 1 deleted"
    }
    ```

`/outlet_groups`


   * `GET`

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


   * `POST`

   ```
    {       
        "name":"group1"
    }
   ```

`/outlet_groups/<outlet_id>`

   * `GET`

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

   * `POST`

   ```
    {       
        "name":"group1"
    }
   ```

   * `DELETE`

   ```
    {
        "message": "group group1 deleted"
    }
   ```

`/outlet_groups/<id>/<outletid>`

   * `PUT`

   ```
    {
        "Success": "added outlet to group"
    }
   ```

   * `DELETE`

   ```
    {
        "Success": "deleted outlet from grouping"
    }
   ```

`/outlet_groups/<id>/users/groups`

   * `POST`

   ```
    {
        "outletgroupid":1,
        "userid":2
    }
   ```

   * `DELETE`

   ```
    {
        "outletgroupid":1,
        "userid":2
    }
   ```

`/outlet_groups/users`

   * `GET`

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

   * `POST`

   ```
    {
        "username":"user1",
        "password":"testpass"
    }
  ```


`/outlet_groups/users/<user_id>`

   * `POST`

   ```
    { 
        "password":"pass"
    }
   ```

   * `DELETE` 

   ```
    {
        "message": "User user1 deleted"
    }
   ```

`/pdu/<pdu_ip>/control`

   * `GET`

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

   * `GET`

   ```
    {
        "amperage": 88, 
        "state": "off"
    }
   ```

   * `POST`

   ```
    {
        "action":"on"
    }
   ```

`/outlet_groups/<id>/control`

   * `POST`

   ```
    {
        "action":"off"
    }
   ```

   * `GET`

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

   * `POST`

   ```
    {
        "action":"off"
    }
   ```

   * `GET`

   ```
    {
        "Status": {
            "10.0.1.33 A 1": "on", 
            "amperage": 63
        }
    }
   ```
