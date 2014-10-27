Igor REST API
=============

A REST API providing endpoints and functions for IPMI control of OSU-OSL machines.

## Quickstart

   * Install required packages:
     * If using pip: `pip install -r requirements.txt`
     * If using easy_install or setuptools: `python setup.py install`
   * If needed, update the database location and credentials in `config.py`
   * Run the server: `python manage.py runserver`
   * Test the running server: `curl -i -u root:root -X GET http://localhost:5000/users`
   * Run automated tests: `nosetests -s`

### Development

If you want to work on the app, you don't want to re-install the app every
time you make a change, you can should install using the following commands:

  * If using pip: `pip install -e -r requirements.txt`
  * If using easy_install or setuptools: `python setup.py develop`

## Design Documents

   * [API Architecture](https://github.com/emaadmanzoor/igor-rest-api/blob/master/docs/API.md)
   * [Serial-on-LAN over REST](https://github.com/emaadmanzoor/igor-rest-api/blob/master/docs/API.md)

## API Documentation

   * [API Usage Examples](https://github.com/emaadmanzoor/igor-rest-api/blob/master/docs/EXAMPLES.md)

## Resources

   * xcat pure Python pyipmi alternative: [python-ipmi](https://github.com/xcat-org/python-ipmi)
   * kontron pure Python pyipmi alternative: [python-ipmi](https://github.com/kontron/python-ipmi)
   * stackforge pure Python pyipmi alternative: [pyghmi](https://github.com/stackforge/pyghmi)
