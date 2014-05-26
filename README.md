Igor REST API
=============

A REST API providing endpoints and functions for IPMI control of OSU-OSL machines.

## Serving

   * Install required packages: `pip install -r requirements.txt`
   * Run the server: `python igor.py`
   * Test the running server: `curl -X GET http://127.0.0.1:5000/hosts`

## Sample Usage

   * Get the list of hosts

```
$ curl -X GET http://127.0.0.1:5000/hosts
{
    "hosts": [
        "osl01"
    ]
}
```

   * View available IPMI operations for a host

```
$ curl -X GET http://127.0.0.1:5000/hosts/osl01
{
    "hostname": "osl01", 
    "operations": [
        "/power/"
    ]
}
```

   * Get the power state of a host

```
$ curl -X GET http://127.0.0.1:5000/hosts/osl01/power
{
    "hostname": "osl01", 
    "power": {
        "state": "off"
    }
}
```

   * Set the power state of a host

```
$ curl -X PUT http://127.0.0.1:5000/hosts/osl01/power/on
{
    "hostname": "osl01", 
    "power": {
        "state": "on"
    }
}
```
