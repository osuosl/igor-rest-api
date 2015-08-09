import cmd
import requests, json, pprint
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError


class Pducmdapp(cmd.Cmd):

    data = []
    username = None
    password = None
    pdu_ip = None
    login = None

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
                r = requests.get('http://localhost:5000/snmplogin',
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

    def do_set_pdu_ip(self, line):
        self.pdu_ip = line
        print 'pdu ip = %s' % self.pdu_ip

    def help_set_pdu_ip(self):
        print 'enter the ip of pdu to be controlled'

    def do_get_pdu_details(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            pdu_ip = line
            url = 'http://localhost:5000/pdu/' + pdu_ip + '/status'
            r = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
            pprint.pprint(r.json())

    def help_get_pdu_details(self):
        print 'will return the status of all outlets and amperage details of pdu'
        print 'usage is get_pdu_details pdu_ip'

    def do_get_status(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            try:
                pdu_ip, line = line.split()
                tower = line[0]
                outlet = line[1]
                if tower not in ['A', 'B', 'a', 'b']:
                    print 'enter vaild tower name'
                else:
                    url = 'http://localhost:5000/pdu/' + pdu_ip + '/' + tower + '/' + outlet
                    r = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
                    pprint.pprint(r.json())
            except:
                print 'usage is get_status pdu_ip A3'

    def help_get_status(self):
        print 'will return the status and amperage of specified outlet'
        print 'usage : get_status pdu_ip A3'

    def do_control_outlet(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        try:
            pdu_ip, temp, state = line.split()
            tower = temp[0]
            outlet = temp[1]
            if (tower not in ['A', 'B', 'a', 'b'] or state not in ['on', 'off', 'reboot']):
                print 'invaild details'
            else:
                url = 'http://localhost:5000/pdu/' + pdu_ip + '/' + tower + '/' + outlet
                data = {'state': state}
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                r = requests.post(url, data=json.dumps(data),
                                  headers=headers, auth=HTTPBasicAuth(self.username, self.password))
                print r.status_code
                pprint.pprint(r.json())
        except:
            print 'usage : control_outlet pdu_ip B5 on/off/reboot'

    def help_control_outlet(self):
        print 'This function can be used to control specific outlets of pdu'
        print 'usage : control_outlet pdu_ip B5 on/off/reboot'

    def do_get_amperage(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        elif self.pdu_ip == None:
            print 'please enter pdu ip using set_pdu_ip'
            return
        else:
            url = 'http://localhost:5000/pdu/' + self.pdu_ip + '/status'
            r = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
            try:
                pprint.pprint(r.json()['amperage'])
            except:
                pprint.pprint(r.json())

        return

    def help_get_amperage(self):
        print 'will return the amperage of pdu'

    def do_list_users(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            url = 'http://localhost:5000/snmpusers'
            r = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
            users = r.json()['users']
            for user in users:
                print user['username']

    def do_create_user(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            try:
                username, password = line.split(':')
            except:
                print 'please enter username and password in username:password form'
                return
            url = 'http://localhost:5000/snmpusers'
            data = {'username': username, 'password': password}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(data), headers=headers, 
                              auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 201:
                pprint.pprint(r.json())
            elif r.status_code == 200:
                pprint.pprint(r.json())
            else:
                print 'unexpected Error'

    def help_create_user(self):
        print 'This can be used to create new user'
        print 'usage is create_user username:password'

    def do_delete_user(self, username):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            url = 'http://localhost:5000/snmpusers/' + username
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.delete(url, headers=headers, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                pprint.pprint(r.json())
            else:
                print 'unexpected response'

    def help_delete_user(self):
        print 'will delete the specified user if you have required permissions'
        print 'usage delete_user username'

    def do_list_pdus(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            url = 'http://localhost:5000/pdus'
            r = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
            pdus = r.json()['pdus']
            for pdu in pdus:
                print pdu['ip']

    def help_list_pdus(self):
        print 'will give list of pdu ips in database'

    def do_create_pdu(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            try:
                hostname, ip, password = line.split(',')
            except ValueError:
                print 'please enter details in hostname,ip,password format'
                return
            url = 'http://localhost:5000/pdus'
            data = {'hostname': hostname, 'ip': ip, 'password': password}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(data), headers=headers,
                              auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 201:
                pprint.pprint(r.json())
            elif r.status_code == 200:
                pprint.pprint(r.json())
            else:
                print 'unexpected Error'

    def help_create_pdu(self):
        print 'Add new pdu entry to database'
        print 'usage is create_pdu pdu_host_name,pdu_ip,pdu_access_string'

    def do_delete_pdu(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            pdu_ip = line
            url = 'http://localhost:5000/pdus/' + pdu_ip
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.delete(url, headers=headers, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                pprint.pprint(r.json())
            else:
                print 'unexpected response'

    def do_get_complete_status(self, line):
        if self.login != True:
            print 'please login to use api'
            return
        else:
            url = 'http://localhost:5000/pdus'
            r = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
            pdus = r.json()['pdus']
            pdu_ips = [pdu['ip'] for pdu['ip'] in pdus]

    def help_delete_pdu(self):
        print 'This can be used to delete pdu from database'
        print 'usage is delete_pdu pdu_ip'

    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    Pducmdapp().cmdloop()
