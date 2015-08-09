import cmd, ast
import requests, json, pprint
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError


class Pducmdapp(cmd.Cmd):
    
    username = None
    password = None
    login = None
    
    # User management
    def do_set_userdetails(self, line):
        try:
            self.username, self.password = line.split(':')
            print 'username is %s' % self.username
            print 'password is %s' % self.password
            login = None
        except:
            print "enter user login details in username:password format"

    def help_set_userdetails(self):
        print 'enter your api login details in username:password format'

    def do_login(self, arg):
        if (self.username or self.password) is None:
            print 'please enter user details using set_user_details'
        else:
            try:
                r = requests.get('http://localhost:5000/outlet_groups/login',
                                auth=HTTPBasicAuth(self.username, self.password))
                if r.status_code == 401:
                    print 'incorrect login details'
                    self.login = False
                elif r.status_code == 200:
                    print 'login details accepted'
                    self.login = True
            except ConnectionError:
                print 'Unable to connect to Api'

    def help_login(self):
        print 'will validate your login details'

    def do_list_users(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            url = 'http://localhost:5000/outlet_groups/users'
            r = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
            users = r.json()['users']
            print "user id's are"
            for user in users:
                print user['userid']

    def do_create_user(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            try:
                line = ast.literal_eval(line)
                if all (key in line for key in ("username", "password")):
                    url = 'http://localhost:5000/outlet_groups/users'
                    data = {'username': line['username'], 'password': line['password']}
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    r = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(self.username, self.password))
                    if r.status_code == 201:
                        pprint.pprint(r.json())
                    else:
                        print 'unexpected Error'
                else:
                    print 'input in wrong format. use help create_user'
            except:
                print 'input in wrong format . use help create_user'
            

    def help_create_user(self):
        print 'This can be used to create new user'
        print 'usage is create_user {"username":"username","password":"user_password"}'

    def do_delete_user(self, userid):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            url = 'http://localhost:5000/outlet_groups/users/' + userid
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.delete(url, headers=headers, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                pprint.pprint(r.json())
            else:
                print 'unexpected response'

    def help_delete_user(self):
        print 'will delete the specified user if you have required permissions'
        print 'usage delete_user userid'

    #  Pdu management
    def do_list_pdus(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            url = 'http://localhost:5000/outlet_groups/pdu'
            r = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
            pdus = r.json()['pdus']
            print 'Pdus list :'
            for pdu in pdus:
                print 'id : ' + str(pdu['id']) + ', ip : ' + pdu['ip']

    def help_list_pdus(self):
        print 'will give list of pdu ips in database'

    def do_create_pdu(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            try:
                line = ast.literal_eval(line)
                if all (key in line for key in ("ip", "access_string")):
                    url = 'http://localhost:5000/outlet_groups/pdu'
                    data = {'ip': line['ip'], 'access_string': line['access_string']}
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    r = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(self.username, self.password))
                    if r.status_code == 201:
                        pprint.pprint(r.json())
                    else:
                        print 'unexpected Error'
                else:
                    print 'input in wrong format. use help create_pdu'
            except:
                print 'input in wrong format . use help create_pdu'

    def help_create_pdu(self):
        print 'Add new pdu entry to database'
        print 'usage is create_pdu {"ip": "pdu_ip","access_string":"pdu_access_string"}'

    def do_delete_pdu(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            pdu_ip = line
            url = 'http://localhost:5000/outlet_groups/pdu/' + pdu_ip
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.delete(url, headers=headers, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                pprint.pprint(r.json())
            else:
                print 'unexpected response'

    def help_delete_pdu(self):
        print 'This can be used to delete pdu from database'
        print 'usage is delete_pdu pdu_ip'

    # group management

    def do_create_group(self, group):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            url = 'http://localhost:5000/outlet_groups'
            data = {'name': group}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 201:
                pprint.pprint(r.json())
            elif r.status_code == 200:
                pprint.pprint(r.json())
            else:
                print 'unexpected Error'

    def help_create_group(self):
        print 'Can be used to create new outlet grouping'
        print 'usage create_group grouping_name'

    def do_list_groups(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            url = 'http://localhost:5000/outlet_groups'
            r = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
            pprint.pprint(r.json()['groups'])

    def help_list_groups(self):
        print 'lists all the groups in database'
        print 'usage list_groups'

    def do_delete_group(self, groupid):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            url = 'http://localhost:5000/outlet_groups/' + groupid
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.delete(url, headers=headers, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                pprint.pprint(r.json())
            else:
                print 'unexpected response'

    def help_delete_group(self):
        print 'deletes the group from database'
        print 'usage is delete_group groupid'

    def do_view_group(self, groupid):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            url = 'http://localhost:5000/outlet_groups/' + groupid
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.get(url, headers=headers, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                pprint.pprint(r.json()['group'])
            else:
                print 'unexpected response'

    def help_view_group(self):
        print 'can be used to view details of specific group'
        print 'usage is view_group groupid'

    # outlet management

    def do_create_outlet(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            try:
                line = ast.literal_eval(line)
                if all (key in line for key in ("pduid", "towername", "outlet")):
                    url = 'http://localhost:5000/outlets'
                    data = {'pduid': line['pduid'], 'towername': line['towername'], 'outlet': line['outlet']}
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    r = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(self.username, self.password))
                    if r.status_code == 201:
                        pprint.pprint(r.json())
                    else:
                        print 'unexpected Error'
                else:
                    print 'input in wrong format. use help create_outlet'
            except:
                print 'input in wrong format . use help create_outlet'

    def help_create_outlet(self):
        print 'this function can be used to create outlet'
        print 'usage is create_outlet {"pduid":pduid,"towername":towername,"outlet":outlet}'

    def do_list_outlets(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            url = 'http://localhost:5000/outlets'
            r = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
            print 'outlets are : '
            pprint.pprint(r.json()['outlets'])

    def help_list_outlets(self):
        print 'will list all the outlets in db'

    def do_delete_outlet(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            url = 'http://localhost:5000/outlets/' + line
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.delete(url, headers=headers, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                pprint.pprint(r.json())
            else:
                print 'unexpected response'

    def help_delete_outlet(self):
        print 'will delete outlet from db'
        print 'usage is delete_outlet outlet_id'

    # outlet group management
    def do_add_outlet_to_group(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            try:
                line = ast.literal_eval(line)
                print line
                if all (key in line for key in ("groupid", "outletid")):
                    url = 'http://localhost:5000/outlet_groups/' + line['groupid'] + '/' + line['outletid']
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    r = requests.put(url, headers=headers, auth=HTTPBasicAuth(self.username, self.password))
                    if r.status_code == 200:
                        pprint.pprint(r.json())
                    else:
                        print 'unexpected Error'
                else:
                    print 'input in wrong format. use help add_outlet_to_group'
            except:
                print 'input in wrong format . use help add_outlet_to_group'

    def help_add_outlet_to_group(self):
        print 'will add outlet to group'
        print 'usage is add_outlet_to_group {"groupid":2,"outletid":3}'

    def do_remove_outlet_from_group(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            try:
                line = ast.literal_eval(line)
                if all (key in line for key in ("groupid", "outletid")):
                    url = 'http://localhost:5000/outlet_groups/' + line['groupid'] + '/' + line['outletid']
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    r = requests.delete(url, headers=headers, auth=HTTPBasicAuth(self.username, self.password))
                    if r.status_code == 200:
                        pprint.pprint(r.json())
                    else:
                        print 'unexpected Error'
                else:
                    print 'input in wrong format. use help remove_outlet_from_group'
            except:
                print 'input in wrong format . use help remove_outlet_from_group'

    def help_remove_outlet_from_group(self):
        print 'will remove outlet from group'
        print 'usage remove_outlet_from_group {"groupid":2,"outletid":3}'

    # group user management

    def do_add_user_to_group(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            try:
                line = ast.literal_eval(line)
                if all (key in line for key in ("outletgroupid", "userid")):
                    url = 'http://localhost:5000/outlet_groups/user/groups'
                    data = {'outletgroupid': line['outletgroupid'], 'userid': line['userid']}
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    r = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(self.username, self.password))
                    if r.status_code == 201:
                        pprint.pprint(r.json())
                    else:
                        print 'unexpected Error'
                else:
                    print 'input in wrong format. use help add_user_to_group'
            except:
                print 'input in wrong format . use help add_user_to_group'

    def help_add_user_to_group(self):
        print 'will associate user to a group'
        print 'usage is add_user_to_group {"outletgroupid":2,"userid":4}'

    def do_remove_user_from_group(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            try:
                line = ast.literal_eval(line)
                if all (key in line for key in ("outletgroupid", "userid")):
                    url = 'http://localhost:5000/outlet_groups/user/groups'
                    data = {'outletgroupid': line['outletgroupid'], 'userid': line['userid']}
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    r = requests.delete(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(self.username, self.password))
                    if r.status_code == 200:
                        pprint.pprint(r.json())
                    else:
                        print 'unexpected Error'
                else:
                    print 'input in wrong format. use help remove_user_from_group'
            except:
                print 'input in wrong format . use help remove_user_from_group'

    def help_remove_user_from_group(self):
        print 'will remove user from group'
        print 'usage is remove_user_from_group {"outletgroupid":2,"userid":4}'

    # control groups

    def do_turn_on_group(self, groupid):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            if groupid == '':
                print 'usage turn_on_group groupid'
                return
            url = 'http://localhost:5000/outlet_groups/' + groupid + '/control'
            data = {'action': 'on'}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                pprint.pprint(r.json())
            else:
                print 'unexpected response'

    def help_turn_on_group(self):
        print 'will switch on all the outlets belonging to a group'
        print 'usage turn_on_group groupid'

    def do_turn_off_group(self, groupid):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            if groupid == '':
                print 'usage turn_off_group groupid'
                return
            url = 'http://localhost:5000/outlet_groups/' + groupid + '/control'
            data = {'action': 'off'}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                pprint.pprint(r.json())
            else:
                print 'unexpected response'

    def help_turn_off_group(self):
        print 'will switch off all the outlets belonging to a group'
        print 'usage turn_off_group groupid'

    def do_reboot_group(self, groupid):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            if groupid == '':
                print 'usage reboot_group groupid'
                return
            url = 'http://localhost:5000/outlet_groups/' + groupid + '/control'
            data = {'action': 'reboot'}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                pprint.pprint(r.json())
            else:
                print 'unexpected response'

    def help_reboot_group(self):
        print 'will reboot all the outlets belonging to a group'
        print 'usage reboot_group groupid'

    def do_get_group_status(self, groupid):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            if groupid == '':
                print 'usage get_group_status groupid'
                return
            url = 'http://localhost:5000/outlet_groups/' + groupid + '/control'
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, headers=headers, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                pprint.pprint(r.json())
            else:
                print 'unexpected response'

    # outlet control
    def do_turn_on_outlet(self, outletid):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            if outletid == '':
                print 'usage turn_on_outlet outletid'
                return
            url = 'http://localhost:5000/outlet/' + outletid + '/control'
            data = {'action': 'on'}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                pprint.pprint(r.json())
            else:
                print 'unexpected response'

    def help_turn_on_outlet(self):
        print 'will switch on the outlets '
        print 'usage turn_on_outlet outletid'

    def do_turn_off_outlet(self, outletid):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            if outletid == '':
                print 'usage turn_off_outlet outletid'
                return
            url = 'http://localhost:5000/outlet/' + outletid + '/control'
            data = {'action': 'off'}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                pprint.pprint(r.json())
            else:
                print 'unexpected response'

    def help_turn_off_outlet(self):
        print 'will switch off the outlets '
        print 'usage turn_off_outlet outletid'

    def do_reboot_outlet(self, outletid):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            if outletid == '':
                print 'usage reboot_outlet outletid'
                return
            url = 'http://localhost:5000/outlet/' + outletid + '/control'
            data = {'action': 'reboot'}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                pprint.pprint(r.json())
            else:
                print 'unexpected response'

    def help_reboot_outlet(self):
        print 'will reboot the outlets '
        print 'usage reboot_group groupid'

    def do_get_outlet_status(self, outletid):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            if outletid == '':
                print 'usage get_outlet_status outletid'
                return
            url = 'http://localhost:5000/outlet/' + outletid + '/control'
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, headers=headers, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                pprint.pprint(r.json())
            else:
                print 'unexpected response'

    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    Pducmdapp().cmdloop()
