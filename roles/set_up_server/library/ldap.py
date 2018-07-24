#!/usr/bin/python
from ansible.module_utils.basic import *
import ldap3
import json

DOCUMENTATION = '''
module: ldap
short_description: "This is a module for modifying entries on LDAP servers."
description: 
 - This  module is used to add, sesarch or delete users and entries on an LDAP server.
 - name is entry distinguishing name (dn)

author:
 - Eyal Engel
requirements:
 - python 2.7 standard library
 - ldap3 package from pypi version ()

options:
  mode: 
    description:
     - choose input mode, options are: dn       - for using the entry dn
				       friendly - for using gn, sn, ou    ( firstName, lastName, organizationalUnit)
       required: true
       defualt: null
{
.
.
.}
'''

EXAMPLES = '''
 Example action to add a user, if doesn't exist
   tasks:
    - name: test the module    with friendly version
      ldap: 
        mode:
          friendly:
            firstname: 'char_temp3'               # aliases don't work the way i want them to :(
            lastname: "Ash's"                     # this example won't run. 
            groups: 'Fire, Pokemon'
        state: present 
        admin_pass: 1


    - name: test the module    with friendly version
      ldap: 
        mode:
          friendly:
            gn: 'char_temp3'
            sn: "Ash's"
            ou: 'Fire, Pokemon'
        state: present 
        admin_pass: 1



   - name: test the module      with dn
      ldap: 
        mode:
          dn:
            dn:  'cn=Bal temp2,ou=Water,ou=Pokemon,dc=localdomain'
        state: present 
        admin_pass: 1

'''
# module does not support check mode... (yet)


class Ldap(object):
	"""
	This is an Ldap server manipulation Class. it is used to convey all the needed information and variables.
	"""
	def __init__(self, module):
		self._module            = module
		self.mode               = "" 
		self.state              = module.params['state']
		self.path               = module.params['path']
		self.admin_pass         = module.params['admin_pass']
		self.admin_dn           = module.params['admin_cn'] + ',dc=' + module.params['server_domain']
		self.server_hostname    = module.params['server_hostname']
		self.server_domain      = module.params['server_domain']
		self.dn	                = ""
		self.gn	                = ""
		self.cn	                = ""
		self.sn                 = ""
		self.ou_list            = [] 
		self.complete_obj()
	

	def complete_obj(self):
		# user data can be specified in two modes.
		# this function is here to complete the missing data, so all object's parameters can always be accessed.
		# please note that this function assumes the data is valid with LDAP (RFC...)

		if bool(self._module.params['mode']['dn']):
			self.mode = 'dn'
			self.complete_friendly()
		elif bool(self._module.params['mode']['friendly']):
			self.mode = 'friendly'
			self.complete_dn()
		else:
			raise NotImplementedError


	def complete_friendly(self):
		# if data was inserted using dn mode, complete the friendly data.
		self.dn = self._module.params['mode']['dn']['dn']
		for pair in self.dn.split(','):				    # pair looks like cn=example
			for attr, value in pair.split('='):
				if attr == 'cn':
					self.cn = value
				if attr == 'ou':
					self.ou_list.append(value)
				if attr == 'cn':			
					self.cn = value
					self.gn, self.sn = value.split(' ') # split commonName to givenName, Surname
									    # if this confuses you, read about LDAP.


	def complete_dn(self):
		# if data was unserted using friendly mode, complete the dn data.
		self.gn = self._module.params['mode']['friendly']['gn']
		self.sn = self._module.params['mode']['friendly']['sn']
		# ou will be handled as a list, in order to maintain code unity and controll.
		self.ou_list.extend(self._module.params['mode']['friendly']['ou'].replace(' ','').split(',')) 
		self.cn = self.gn + ' ' + self.sn
		self.dn = "cn={cn},ou={ou},dc={dc}".format(cn=self.cn, ou=',ou='.join(self.ou_list), dc=self.server_domain)        # build dn




def connect(server, user_dn, passphrase):
	# this function is used to connect and authenticate against the LDAP server.
	# would normally write a "build_DN" function, but this is used only once. other DNs should come complete from input.	
	
	conn = ldap3.Connection(server, user_dn, passphrase, auto_bind=True)
	return conn


def search_entry(conn, search_filter, search_base):
	# a very simple wrapper function to provide default values.
	return conn.search(search_base, search_filter)


def is_present(conn, dn):
	# function checks if a provided dn existss in DIT
	# LDAP does not support searching by dn, therefore we send dn as the base of the search, and see
	# if any object exists under it.
	s_filter = '(objectClass=*)'                			                        # any entry will be valid with this filter                      
	present = search_entry(conn, s_filter, search_base=dn)
	return bool(present)


def add_user(conn, dn, **kwargs):
	# function will add a user entry to DIT, if it doesn't exist already, arguments cn, sn are necessary.
	# function assumes all users are of objectClass inetOrgPerson, and does not validate input.
	if (not is_present(conn, dn)):
		success = conn.add(dn, 'inetOrgPerson', kwargs)
		assert success
		return True
	else:
		return False



def main():
	# what if a dumb user wants to add like this:  "name=Balbazor element=Water"
	# answer: user will choose to define name either by dn, or by first & last names and groups.
	# deleted will prob. not be supported
	module = AnsibleModule(
		argument_spec = dict(
			mode = dict(										# name:
				required = True, 
				type = 'dict',
			 	options = dict(
					dn = dict(								# use dn
						dn = dict(required = True, aliases = ['name'])),
					friendly = dict(							# use friendy names
						gn = dict(required=True, aliases=['firstname', 'givenName']),	    
						sn = dict(required=True, aliases=['surname']),		
						ou = dict(required=True, aliases=['groups', 'organizationalUnit']),
						type='dict'
					),
				)
			),
			state = dict(required=True, choices=['present', 'absent', 'searched']),       # serached will output a file
			path = dict(required=False, default='~/'),                                    # should i use required?   used to output
			admin_cn = dict(required=True),
			admin_pass = dict(required=True),
			server_hostname = dict(reqired=True),
			server_domain = dict(reqired=True)
		)
	)	

	try:
		ldap = Ldap(module)
	except Exception as e:	
		module.fail_json(msg='failed to create  Ldap object', exp=e)
	server_address = ldap.server_hostname + '.' + ldap.server_domain

	try:
		conn = connect(server_address, ldap.admin_dn, ldap.admin_pass)	
	except Exception as e:
		module.fail_json(msg="Connection to server was unseccessful.\n" + str(e))            # here to test output

	try:
		added = add_user(conn, ldap.dn, sn=ldap.sn, gn=ldap.gn)
	except AssertionError as ae:	
		module.fail_json(msg="Entry Addition Query was unseccessful." + str(conn))
	except Exception as e:
		print json.dumps({"failed": True, "msg": e})
		module.fail_json(msg="Something bad happend.")
	if added:
		module.exit_json(changed=True)							      # perhaps add message beyond ansible's default?
	else:
		module.exit_json(changed=False)


if __name__ == '__main__':
	main()


