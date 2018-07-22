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
