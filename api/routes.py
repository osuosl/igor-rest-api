from api import app
from flask.ext import restful

# Dummy data, should be retrieved from a database eventually
hosts = [{'hostname': 'osl01',
          'operations': ['/power/'],
          'power': {
              'state': 'off'
          }
        }]

igor_api = restful.Api(app)

class HostListAPI(restful.Resource):
    def get(self):
        return {'hosts': [host['hostname'] for host in hosts]}

    def post(self):
        pass

class HostAPI(restful.Resource):
    def get(self, hostname):
        for host in hosts:
            if host['hostname'] == hostname:
                return {'hostname': hostname,
                        'operations': host['operations']}

class HostPowerAPI(restful.Resource):
    def get(self, hostname):
        for host in hosts:
            if host['hostname'] == hostname:
                return {'hostname': hostname,
                        'power': host['power']}

    def put(self, hostname, action):
        for host in hosts:
            if host['hostname'] == hostname:
                host['power'] = action
                return {'hostname': hostname,
                        'power': host['power']}

igor_api.add_resource(HostListAPI, '/hosts', endpoint='hosts')
igor_api.add_resource(HostAPI, '/hosts/<string:hostname>', endpoint='host')
igor_api.add_resource(HostPowerAPI, '/hosts/<string:hostname>/power', endpoint='host_power_get')
igor_api.add_resource(HostPowerAPI, '/hosts/<string:hostname>/power/<string:action>', endpoint='host_power_put')
