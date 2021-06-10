#!/usr/bin/python
# -*- coding: utf-8 -*-

# (C) Copyright 2019-2020 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'certified'
}

DOCUMENTATION = '''
---
module: aoscx_acl_interface
version_added: "2.8"
short_description: Apply/Remove ACL configuration on interfaces for AOS-CX.
description:
  - This modules provides application management of Access Classifier Lists
    on Interfaces on AOS-CX devices.
author: Aruba Networks (@ArubaNetworks)
options:
  acl_name:
    description: Name of the ACL being applied or removed from the interface.
    required: true
    type: str

  acl_type:
    description: Type of ACL being applied or removed from the interfaces.
    choices: ['ipv4', 'ipv6', 'mac']
    required: true
    type: str

  acl_interface_list:
    description: List of interfaces for which the ACL is to be applied or
      removed.
    required: true
    type: list

  acl_direction:
    description: Direction for which the ACL is to be applied or removed.
    required: true
    choices: ['in', 'out']
    default: 'in'
    type: str

  state:
    description: Create or delete the ACL configuration from the interfaces.
    required: false
    choices: ['create', 'delete']
    default: create
    type: str
'''

EXAMPLES = '''
- name: Apply ipv4 ACL to interfaces
  aoscx_acl_interface:
    acl_name: ipv4_acl
    acl_type: ipv4
    acl_interface_list: ["1/1/2", "1/2/23"]

- name: Remove ipv4 ACL from interfaces
  aoscx_acl_interface:
    acl_name: ipv4_acl
    acl_type: ipv4
    acl_interface_list: ["1/1/2", "1/2/23"]
    state: delete

- name: Apply ipv6 ACL to Interfaces
  aoscx_acl_interface:
    acl_name: ipv6_acl
    acl_type: ipv6
    acl_interface_list: ["1/1/2", "1/2/23"]
'''

RETURN = r''' # '''

from ansible.module_utils.aoscx_port import Port
from ansible.module_utils.aoscx_interface import Interface
from ansible.module_utils.aoscx import ArubaAnsibleModule

def main():
    module_args = dict(
        acl_name=dict(type='str', required=True),
        acl_type=dict(type='str', required=True, choices=['ipv4',
                                                          'ipv6', 'mac']),
        acl_interface_list=dict(type='list', required=True),
        acl_direction=dict(type='str', default='in', choices=['in', 'out']),
        state=dict(type='str', default='create', choices=['create', 'delete'])
    )

    # Version management
    try:

        from ansible.module_utils.aoscx_pyaoscx import Session
        from pyaoscx.session import Session as Pyaoscx_Session
        from pyaoscx.pyaoscx_factory import PyaoscxFactory

        USE_PYAOSCX_SDK = True

    except ImportError:
        USE_PYAOSCX_SDK = False

    # Use PYAOSCX SDK
    if USE_PYAOSCX_SDK:
        from ansible.module_utils.basic import AnsibleModule

        # ArubaModule
        ansible_module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True)

        # Session
        session = Session(ansible_module)

        # Set Variables
        acl_name = ansible_module.params['acl_name']
        acl_interface_list = ansible_module.params['acl_interface_list']  # NOQA
        acl_type = ansible_module.params['acl_type']
        acl_direction = ansible_module.params['acl_direction']
        state = ansible_module.params['state']

        result = dict(
            changed=False
        )

        if ansible_module.check_mode:
            ansible_module.exit_json(**result)

        # Get session serialized information
        session_info = session.get_session()
        # Create pyaoscx.session object
        s = Pyaoscx_Session.from_session(
            session_info['s'], session_info['url'])

        # Create a Pyaoscx Factory Object
        pyaoscx_factory = PyaoscxFactory(s)

        for interface_name in acl_interface_list:
            if state == 'delete':
                # Create ACL Object
                interface = pyaoscx_factory.interface(interface_name)
                # Delete it
                interface.clear_acl(acl_type)
                # Changed
                result['changed'] = True

            if state == 'create' or state == 'update':
                # Create ACL Object
                interface = pyaoscx_factory.interface(interface_name)
                # Verify if interface was create
                if interface.was_modified():
                    # Changed
                    result['changed'] = True

                # Modified variables
                modified_op1 = False
                modified_op2 = False
                # Update ACL inside Interface
                if acl_direction == 'in':
                    modified_op1 = interface.update_acl_in(
                        acl_name, acl_type)
                if acl_direction == 'out':
                    modified_op2 = interface.update_acl_out(
                        acl_name, acl_type)
                if modified_op1 or modified_op2:
                    # Changed
                    result['changed'] = True

        # Exit
        ansible_module.exit_json(**result)

    # Use Older version
    else:

        aruba_ansible_module = ArubaAnsibleModule(module_args)

        acl_name = aruba_ansible_module.module.params['acl_name']
        acl_interface_list = aruba_ansible_module.module.params['acl_interface_list']  # NOQA
        acl_type = aruba_ansible_module.module.params['acl_type']
        acl_direction = aruba_ansible_module.module.params['acl_direction']
        state = aruba_ansible_module.module.params['state']

        interface = Interface()
        port = Port()

        for interface_name in acl_interface_list:
            if not port.check_port_exists(
                    aruba_ansible_module, interface_name):
                aruba_ansible_module.module.fail_json(
                    msg="Interface {int} is not configured".format(
                        int=interface_name))

            if (state == 'create') or (state == 'update'):
                update_type = 'insert'
            elif (state == 'delete'):
                update_type = 'delete'
            aruba_ansible_module = interface.update_interface_acl_details(
                aruba_ansible_module, interface_name, acl_name, acl_type,
                acl_direction, update_type)

            if update_type == 'insert':
                aruba_ansible_module.module.log(
                    msg="Attached ACL {acl} of type "
                    "{type} to interface {int}"
                    "".format(
                        acl=acl_name,
                        type=acl_type,
                        int=interface_name))

            if update_type == 'update':
                aruba_ansible_module.module.log(
    msg="Updated ACL {acl} of type "
    "{type} attached to interface"
    " {int}"
    "".format(
        acl=acl_name,
        type=acl_type,
         int=interface_name))  # NOQA

            if (update_type == 'absent') or (update_type == 'delete'):
                aruba_ansible_module.module.log(
                    msg="Removed ACL {acl} of type"
                    " {type} from interface"
                    " {int}"
                    "".format(
                        acl=acl_name,
                        type=acl_type,
                        int=interface_name))

        aruba_ansible_module.update_switch_config()


if __name__ == '__main__':
    main()
