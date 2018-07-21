#!/usr/bin/python

from ansible.module_utils.basic import *
import ldap3


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
	s_filter = '(objectclass=*)'                				# any entry will be valid with this filter                      
	present = search_entry(conn, s_filter, search_base=dn)
	return present




def main():

	module = AnsibleModule(
		argument_spec = dict(
			name = dict(required=True),				                      # deleted will prob. not be supported
			state = dict(required=True, choices=['present', 'absent', 'searched']),       # serached will output a file
			path = dict(required=False, default='~/'),                                    # should i use required?
		)
#		support_check_mode=True
	)
	conn = connect()	
	module.fail_json(msg="Something bad happend.\n" + str(conn))   # here to test output


# Successful exit:
#module.exit_json(changed=true, additional_data="Ansible is cool!")

# Unsuccessful exit:
#module.fail_json(msg="Something bad happend.")                    # msg is a must

#from ansible.module_utils.basic import *
if __name__ == '__main__':
	main()


