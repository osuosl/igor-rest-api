Igor REST API
=============

A REST API providing endpoints and functions for IPMI, SNMP control of OSU-OSL machines.

## Quickstart

   * Install required packages:
     * If using pip: `pip install -r requirements.txt`
     * If using easy_install or setuptools: `python setup.py install`
   * If needed, update the database location and credentials in `igor_rest_api/config.py`
   * Create the database schema, and root user: `igor-manage init_db`
   * Run the server: `igor-manage runserver`
   * Test the running server: `curl -i -u root:root -X GET http://localhost:5000/users`
   * Run tests: `python setup.py test` or `python setup.py nosetests` for more options.

### Development

If you want to work on the app, you don't want to re-install the app every
time you make a change, you can should install using the following commands:

  * If using pip: `pip install -e -r requirements.txt`
  * If using easy_install or setuptools: `python setup.py develop`

Running the test server locally can be done using `manage.py` or `igor-manage`

   * `python manage.py runserver`
   * `igor-manage runserver`

## Design Documents

   * [API Architecture](docs/API.md)
   * [Serial-on-LAN over REST](docs/SOL.md)

## API Documentation

   * [IPMI API Usage Examples](docs/EXAMPLES.md)
   * [SNMP API Usage Examples](docs/Groupings.md)

## Resources

   * xcat pure Python pyipmi alternative: [python-ipmi](https://github.com/xcat-org/python-ipmi)
   * kontron pure Python pyipmi alternative: [python-ipmi](https://github.com/kontron/python-ipmi)
   * stackforge pure Python pyipmi alternative: [pyghmi](https://github.com/stackforge/pyghmi)
