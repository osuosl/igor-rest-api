Igor REST API
=============

A REST API providing endpoints and functions for IPMI control of OSU-OSL machines.

## Quickstart

   * Install required packages: `pip install -r requirements.txt`
   * If needed, update the database location and credentials in `config.py`
   * Run the server: `python manage.py runserver`
   * Test the running server: `curl -i -u root:root -X GET http://localhost:5000/users`
   * Run automated tests: `nosetests -s`

## Design Documents

   * [API Architecture](https://github.com/emaadmanzoor/igor-rest-api/blob/master/docs/API.md)
   * [Serial-on-LAN over REST](https://github.com/emaadmanzoor/igor-rest-api/blob/master/docs/API.md)
   
## API Documentation

   * [API Usage Examples](https://github.com/emaadmanzoor/igor-rest-api/blob/master/docs/EXAMPLES.md)
