#!/usr/bin/python

from ansible.module_utils.basic import *

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

#from ansible.module_utils.urls import *

# module does not support check mode... (yet)

# note to self: make sure to add full support to LDAP protocol.
def main():
	module = AnsibleModule(
		argument_spec = dict(
			name = dict(required=True),				      # deleted will prob. not be supported
			state = dict(choices=['exist', 'absent', 'searched']),       # serached will output a file
			path = dict(required=False, default='~/'),                    # should i use required?
                        #server = dict(default=inventory_hostname)
		)
#		support_check_mode=True
	)
	module.fail_json(msg="Something bad happend.") 


# Successful exit:
#module.exit_json(changed=true, additional_data="Ansible is cool!")

# Unsuccessful exit:
#module.fail_json(msg="Something bad happend.")                    # msg is a must

#from ansible.module_utils.basic import *
if __name__ == '__main__':
	main()

