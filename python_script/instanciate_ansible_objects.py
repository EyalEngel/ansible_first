#!/usr/bin/env python
#  Ansible: initialize needed objects
variable_manager = VariableManager()
loader = DataLoader()

#  Ansible: Load inventory
inventory = Inventory(
    loader = loader,
    variable_manager = variable_manager,
    host_list = 'hosts', # Substitute your filename here
)