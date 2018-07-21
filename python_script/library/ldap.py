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


def check_args():
	#function makes sure that playbook input is either a dn or a cn + sn + ou combo


def main():
	# what if a dumb user wants to add like this:  "name=Balbazor element=Water"
	# deleted will prob. not be supported

	module = AnsibleModule(
		argument_spec = dict(
			dn = dict(aliases=['name']), 		     				      # either a dn or cn + sn + ou tree is required. couldn't
			cn = dict(aliases=['firstname', 'common_name']),			      # find a way to define this logic here,  so it is 
			sn = dict(aliases=['surname']),						      # impleneted later.
			ou = dict(aliases=['group', 'organizationalUnit']),
			state = dict(required=True, choices=['present', 'absent', 'searched']),       # serached will output a file
			path = dict(required=False, default='~/'),                                    # should i use required?   used to output
		)
		support_check_mode=False
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


