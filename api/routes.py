from api import app
from functools import wraps
from flask import session, url_for, g
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.httpauth import HTTPBasicAuth
from models import db, User, Machine
from pyipmi import make_bmc, IpmiError
from pyipmi.bmc import LanBMC
import jsonpickle

# Define the HTTP error codes we use
OK = 200
CREATED = 201 
BAD_REQUEST = 400 
UNAUTHORIZED = 401 
NOT_FOUND = 404 
FORBIDDEN = 403 

# Constants
TOKEN_EXPIRATION = 600 # 10 minutes

igor_api = Api(app)
auth = HTTPBasicAuth()

# Utility functions
def try_ipmi_command(command, **kwargs):
    try:
        response = command(**kwargs), OK
    except IpmiError as error:
        response = error.message, BAD_REQUEST
    return response

# Authentication, writes g.user
@auth.verify_password
def validate_password(username_or_token, password):
    user = User.validate_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True

# Authorization for the IPMI operations
# Requires g.user and hostname, writes g.machine
def permission_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = g.user

        hostname = kwargs['hostname']
        machine = Machine.query.filter_by(hostname=hostname).first()
        if not machine:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND

        if not user in machine.users:
            return {'message': 'User %s does not have permission for host %s'
                    % (user.username, hostname)}, FORBIDDEN

        g.machine = machine
        return f(*args, **kwargs)
    return decorated

# Login endpoint
"""
    GET     /login            Generates an returns an authentication token
"""
class LoginAPI(Resource):
    decorators = [auth.login_required]
    def get(self):
        token = g.user.generate_auth_token(TOKEN_EXPIRATION)
        return {'token': token.decode('ascii'), 'duration': TOKEN_EXPIRATION}

igor_api.add_resource(LoginAPI, '/login', endpoint='login')

# User management endpoints
"""
    GET     /users                           Returns the list of users
    POST    /users {'username': username,
                    'password': password}    Creates a new user
"""
class UsersAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True,
                                    help='No username provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True,
                                    help='No password provided', location='json')
        super(UsersAPI, self).__init__()

    def get(self):
        users = []
        for user in User.query.all():
            users.append(user.username)
        return {'users': [{'username': username,
                           'location': url_for('user', username=username, _external=True)}
                          for username in users]}

    def post(self):
        args = self.reqparse.parse_args()
        
        username = args['username']
        password = args['password']
        if User.query.filter_by(username=username).first() is not None:
            return {'message': 'User %s exists' % username}, BAD_REQUEST 
        else:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
            return {'username': user.username,
                    'machines': url_for('user_machines', username=username, _external=True),
                    'location': url_for('user', username=user.username, _external=True)}, CREATED
        
"""
    GET     /users/:username             Returns details for user <username>
    DELETE  /users/:username             Deletes user <username>
    PUT     /users/:username             Updates password for user <username>
"""
class UserAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('password', type=str, required=True,
                                    help='No password provided', location='json')
        super(UserAPI, self).__init__()

    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND
        else:
            return {'username': user.username,
                    'machines': url_for('user_machines', username=username, _external=True),
                    'location': url_for('user', username=username, _external=True)}

    def delete(self, username):
        if g.user.username != 'root' and g.user.username != username:
            return {'message': '%s cannot delete user %s' % (g.user.username, username)}

        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND
        else:
            user.machines = []
            db.session.add(user)
            db.session.commit()
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User %s deleted' % user.username}

    def put(self, username):
        if g.user.username != 'root' and g.user.username != username:
            return {'message': '%s cannot modify user %s' % (g.user.username, username)}
        
        args = self.reqparse.parse_args()
        user = User.query.filter_by(username=username).first()
        password = args['password']
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND
        else:
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return {'message': 'Updated entry for user %s' % username}

igor_api.add_resource(UsersAPI, '/users', endpoint='users')
igor_api.add_resource(UserAPI, '/users/<string:username>', endpoint='user')

# Machine management endpoints
"""
    GET     /machines                           Returns the list of machines
    POST    /machines {'hostname': hostname,
                       'username': username,
                       'fqdn':     FQDN,
                       'password': password}    Creates a new machine entry
"""
class MachinesAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('hostname', type=str, required=True,
                                    help='No hostname provided', location='json')
        self.reqparse.add_argument('fqdn', type=str, required=True,
                                    help='No FQDN provided', location='json')
        self.reqparse.add_argument('username', type=str, required=True,
                                    help='No username provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True,
                                    help='No password provided', location='json')
        super(MachinesAPI, self).__init__()

    def get(self):
        machines = []
        for machine in Machine.query.all():
            machines.append(machine.hostname)
        return {'machines': [{'hostname': hostname,
                              'users': url_for('machine_users', hostname=hostname, _external=True),
                              'location': url_for('machine', hostname=hostname, _external=True)}
                              for hostname in machines]}

    def post(self):
        args = self.reqparse.parse_args()

        hostname = args['hostname']
        fqdn = args['fqdn']
        username = args['username']
        password = args['password']
        if Machine.query.filter_by(hostname=hostname).first() is not None:
            return {'message': 'Host %s exists' % hostname}, BAD_REQUEST
        else:
            machine = Machine(hostname, fqdn, username, password)
            db.session.add(machine)
            db.session.commit()
            return {'hostname': machine.hostname,
                    'users': url_for('machine_users', hostname=hostname, _external=True),
                    'location': url_for('machine', hostname=machine.hostname, _external=True)}, CREATED

"""
    GET     /machines/:hostname             Returns details for machine <hostname>
    DELETE  /machines/:hostname             Deletes machine <hostname>
    PUT     /machines/:hostname             Updates FQDN, username and password for machine <hostname>
"""
class MachineAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('fqdn', type=str, required=True,
                                    help='No FQDN provided', location='json')
        self.reqparse.add_argument('username', type=str, required=True,
                                    help='No username provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True,
                                    help='No password provided', location='json')
        super(MachineAPI, self).__init__()

    def get(self, hostname):
        machine = Machine.query.filter_by(hostname=hostname).first()
        if not hostname:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND
        else:
            return {'hostname': machine.hostname,
                    'fqdn': machine.fqdn,
                    'users': url_for('machine_users', hostname=hostname, _external=True),
                    'location': url_for('machine', hostname=hostname, _external=True)}

    def delete(self, hostname):
        machine = Machine.query.filter_by(hostname=hostname).first()
        if not machine:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND
        else:
            machine.users = []
            db.session.add(machine)
            db.session.commit()
            db.session.delete(machine)
            db.session.commit()
            return {'message': 'Host %s deleted' % machine.hostname}

    def put(self, hostname):
        args = self.reqparse.parse_args()
        machine = Machine.query.filter_by(hostname=hostname).first()
        fqdn = args['fqdn']
        username = args['username']
        password = args['password']
        if not machine:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND
        else:
            machine.fqdn = fqdn
            machine.username = username
            machine.password = password
            db.session.add(machine)
            db.session.commit()
            return {'message': 'Updated entry for host %s' % hostname}

igor_api.add_resource(MachinesAPI, '/machines', endpoint='machines')
igor_api.add_resource(MachineAPI, '/machines/<string:hostname>', endpoint='machine')

# Machine-user permissions endpoints
"""
    GET     /users/:username/machines               Returns the list of machines accessible by :username
"""
class UserMachinesAPI(Resource):
    decorators = [auth.login_required]

    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND
        return {'username': user.username,
                'machines': [{'hostname': machine.hostname,
                              'location': url_for('machine', hostname=machine.hostname, _external=True)}
                              for machine in user.machines]}

"""
    GET     /users/:username/machines/:hostname     Returns 200 or 404, depending on :username's access to :hostname
    PUT     /users/:username/machines/:hostname     Adds :username-:hostname entry to the permissions table
    DELETE  /users/:username/machines/:hostname     Deletes :username-:hostname entry in the permissions table  
"""
class UserMachineAPI(Resource):
    decorators = [auth.login_required]

    def get(self, username, hostname):
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND

        machine = Machine.query.filter_by(hostname=hostname).first()
        if not machine:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND

        if machine in user.machines:
            return {'username': username,
                    'hostname': hostname,
                    'location': url_for('machine', hostname=hostname, _external=True)}
        else:
            return {'message': 'User %s does not have permission for host %s' % (username, hostname)}, NOT_FOUND

    def put(self, username, hostname):
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND

        machine = Machine.query.filter_by(hostname=hostname).first()
        if not machine:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND

        if machine not in user.machines:
            user.machines.append(machine)
            db.session.add(user)
            db.session.commit()

        return {'message': 'Created permission for user %s to host %s' % (username, hostname)}, CREATED

    def delete(self, username, hostname):
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND

        machine = Machine.query.filter_by(hostname=hostname).first()
        if not machine:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND

        if machine in user.machines:
            user.machines.remove(machine)
            db.session.add(user)
            db.session.commit()

            return {'message': 'Deleted permission for user %s to host %s' % (username, hostname)}
        else:
            return {'message': 'User %s does not have permission for host %s' % (username, hostname)}, NOT_FOUND

"""
    GET     /machines/:hostname/users               Returns the list of users with access to :hostname
"""
class MachineUsersAPI(Resource):
    decorators = [auth.login_required]

    def get(self, hostname):
        machine = Machine.query.filter_by(hostname=hostname).first()
        if not machine:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND

        return {'hostname': machine.hostname,
                'users': [{'username': user.username,
                           'location': url_for('user', username=user.username, _external=True)}
                            for user in machine.users]}

"""
    GET     /machines/:hostname/users/:username     Returns 200 or 404, depending on :username's access to :hostname
    PUT     /machines/:hostname/users/:username     Adds :username-:hostname entry to the permissions table
    DELETE  /machines/:hostname/users/:username     Deletes :username-:hostname entry in the permissions table  
"""
class MachineUserAPI(Resource):
    decorators = [auth.login_required]

    def get(self, hostname, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND

        machine = Machine.query.filter_by(hostname=hostname).first()
        if not machine:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND

        if user in machine.users:
            return {'username': username,
                    'hostname': hostname,
                    'location': url_for('user', username=username, _external=True)}
        else:
            return {'message': 'User %s does not have permission for host %s' % (username, hostname)}, NOT_FOUND

    def put(self, hostname, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND

        machine = Machine.query.filter_by(hostname=hostname).first()
        if not machine:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND

        if user not in machine.users:
            machine.users.append(user)
            db.session.add(machine)
            db.session.commit()

        return {'message': 'Created permission for user %s to host %s' % (username, hostname)}, CREATED

    def delete(self, hostname, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND

        machine = Machine.query.filter_by(hostname=hostname).first()
        if not machine:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND

        if user in machine.users:
            machine.users.remove(user)
            db.session.add(machine)
            db.session.commit()

            return {'message': 'Deleted permission for user %s to host %s' % (username, hostname)}
        else:
            return {'message': 'User %s does not have permission for host %s' % (username, hostname)}, NOT_FOUND

igor_api.add_resource(UserMachinesAPI, '/users/<string:username>/machines', endpoint='user_machines')
igor_api.add_resource(UserMachineAPI, '/users/<string:username>/machines/<string:hostname>', endpoint='user_machine')
igor_api.add_resource(MachineUsersAPI, '/machines/<string:hostname>/users', endpoint='machine_users')
igor_api.add_resource(MachineUserAPI, '/machines/<string:hostname>/users/<string:username>', endpoint='machine_user')

# IPMI Operations
class IPMIResource(Resource):
    decorators = [permission_required, auth.login_required]

    def __init__(self):
        self.bmc = make_bmc(LanBMC, hostname=g.machine.fqdn,
                            username=g.machine.username,
                            password=g.machine.password)
        super(IPMIResource, self).__init__()

"""
    GET     /machines/:hostname/chassis     Gets the chassis status
"""
class MachineChassisAPI(IPMIResource):

    def get(self, hostname):
        ipmi_response = try_ipmi_command(self.bmc.get_chassis_status)
        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, BAD_REQUEST

        response = ipmi_response[0].__dict__
        response['hostname'] = hostname
        return response

igor_api.add_resource(MachineChassisAPI, '/machines/<string:hostname>/chassis', endpoint='machine_chassis')

"""
    GET     /machines/:hostname/chassis/power     Gets the chassis power status
    POST    /machines/:hostname/chassis/power
            {'power': 'on'|'off'|'cycle}          Sets the chassis power
"""
class MachineChassisPowerAPI(IPMIResource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('power', type=str, required=True,
                                    help='No power status provided',
                                    location='json')
        super(MachineChassisPowerAPI, self).__init__()

    def get(self, hostname):
        ipmi_response = try_ipmi_command(self.bmc.get_chassis_status)
        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, BAD_REQUEST

        power_on = ipmi_response[0].power_on
        if power_on:
            power_status = 'on'
        else:
            power_status = 'off'

        return {'hostname': hostname, 'power': power_status}

    def post(self, hostname):
        args = self.reqparse.parse_args()
        power_status = args['power']

        ipmi_response = try_ipmi_command(self.bmc.set_chassis_power,
                                         mode=power_status)
        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, BAD_REQUEST

        return {'hostname': hostname,
                'message': 'Power status set to %s' % power_status}

igor_api.add_resource(MachineChassisPowerAPI, '/machines/<string:hostname>/chassis/power', endpoint='machine_chassis_power')
