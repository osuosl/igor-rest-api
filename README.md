Igor REST API
=============

A REST API providing endpoints and functions for IPMI control of OSU-OSL machines.

## Quickstart

   * Install required packages: `pip install -r requirements.txt`
   * Update the database credentials in `api/config.py`
   * `TODO` Create the database and entries: `python api/migrate.py`
   * Run the server: `python runserver.py`
   * Test the running server: `curl -i -u root:root -X GET http://localhost:5000/hosts`

## [API Design & Architecture](https://github.com/emaadmanzoor/igor-rest-api/blob/master/docs/API.md)

## [API Usage Examples](https://github.com/emaadmanzoor/igor-rest-api/blob/master/docs/EXAMPLES.md)
