#!/usr/bin/python

from ansible.module_utils.basic import *
import ldap3
import json

import socket
ADDRESS = socket.gethostname()                     # prob. not the best way, the best one i found.
HOST_NAME, DOMAIN_NAME = ADDRESS.split('.')	   # assuming code will be run on every target machine.

ADMIN_DN = "cn=Manager,dc=" + DOMAIN_NAME
ADMIN_PASS = '1'






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
  name: 
    description:
     - the entry dn
       required: true
       defualt: null
{
.
.
.}
'''

EXAMPLES = '''
# Example action to add a user, if doesn't exist
 - ldap:
     name: {paste}
     state: exist
'''


# module does not support check mode... (yet)
# note to self: make sure to add full support to LDAP protocol.


class Ldap(object):
	"""
	This is an Ldap server manipulation Class. it is used to convey all the needed information and variables.
	"""
	def __init__(self, module):
		self._module  = module
		self.dn       = module.params['dn']
		self.cn       = module.params['cn']
		self.sn       = module.params['sn']
		self.ou       = module.params['ou']
		self.state    = module.params['state']
		self.path     = module.params['path']



def connect(server=ADDRESS, user_dn=ADMIN_DN, passphrase=ADMIN_PASS):
	# this function is used to connect and authenticate against the LDAP server.
	# would normally write a "build_DN" function, but this is used only once. other DNs should come complete from input.	
	
	conn = ldap3.Connection(server, user_dn, passphrase, auto_bind=True)
	return conn


def search_entry(conn, serach_filter, search_base=DOMAIN_NAME):
	# a very simple wrapper function to provide default values.
	conn.search(search_base, search_filter)


def is_present(conn, dn):
	# function checks if a provided dn existss in DIT
	# LDAP does not support searching by dn, therefore we send dn as the base of the search, and see
	# if any object exists under it.
	s_filter = '(objectclass=*)'                			                        # any entry will be valid with this filter                      
	present = search_entry(conn, s_filter, search_base=dn)
	return present


def add_user(conn, dn, **kwargs):
	# function will add a user entry to DIT, if it doesn't exist already, arguments cn, sn are necessary.
	# function assumes all users are of objectClass inetOrgPerson, and does not validate input.
	if (not is_present(conn, dn)):
		success = conn.add(dn, 'inetOrgPerson', kwargs)
		assert success


def main():
	# what if a dumb user wants to add like this:  "name=Balbazor element=Water"
	# answer: user will choose to define name either by dn, or by first & last names and groups.
	# deleted will prob. not be supported
	
	module = AnsibleModule(
		argument_spec = dict(
			name = dict(										# name:
				required = True, 
				type = 'dict',
			 	options = dict(
					dn = dict(								# use dn
						dn = dict(required = True, aliases = ['name'])),
					friendly = dict(							# use friendy names
						gn = dict(required=True, aliases=['firstname', 'givenName']),	    
						sn = dict(required=True, aliases=['surname']),		
						ou = dict(required=True, aliases=['groups', 'organizationalUnit']),
					)
				)
			),
			state2 = dict(required=True, choices=['present', 'absent', 'searched']),       # serached will output a file
			path = dict(required=False, default='~/'),                                    # should i use required?   used to output
		),
		supports_check_mode=False
	)	


	ldap = Ldap(module)


	conn = connect()	
	
	
	try:
		#add_user(conn, ............)
		print json.dumps({"msg": "not yet"})
		module.exit_json(changed=True)							      # perhaps add message beyond ansible's default?

	except AssertionError:	
		module.fail_json(msg="Entry Addition Query was unseccessful." + str(conn))            # here to test output
	except Exception as e:
		print json.dumps({"failed": True, "msg": e})
		module.fail_json(msg="Something bad happend.")
		


# Successful exit:
#module.exit_json(changed=true, additional_data="Ansible is cool!")

# Unsuccessful exit:
#module.fail_json(msg="Something bad happend.")                    # msg is a must

#from ansible.module_utils.basic import *
if __name__ == '__main__':
	main()


