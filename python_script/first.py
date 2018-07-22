#!/usr/bin/python

from ansible.module_utils.urls import *

# module does not support check mode... (yet)

# note to self: make sure to add full support to LDAP protocol.
def main():
	module = AnsibleModule(
		argument_spec = dict(
			name = dict(required=True)				   # deleted will prob. not be supported
			state = dict(choices=['added', 'deleted', 'searched'])       # serached will output a file
			path = dict(required=False, default='~/')                    # should i use required?
		)
#		support_check_mode=True
	)
# Successful exit:
#module.exit_json(changed=true, additional_data="Ansible is cool!")

# Unsuccessful exit:
#module.fail_json(msg="Something bad happend.")                    # msg is a must

from ansible.module_utils.basic import *
if __name__ == '__main__':
	main()
