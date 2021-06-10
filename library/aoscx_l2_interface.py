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
module: aoscx_l2_interface
version_added: "2.8"
short_description: Create or Update or Delete Layer2 Interface configuration on AOS-CX
description:
  - This modules provides configuration management of Layer2 Interfaces on
    AOS-CX devices.
author: Aruba Networks (@ArubaNetworks)
options:
  interface:
    description: Interface name, should be in the format chassis/slot/port,
      i.e. 1/2/3 , 1/1/32. Please note, if the interface is a Layer3 interface
      in the existing configuration and the user wants to change the interface
      to be Layer2, the user must delete the L3 interface then recreate the
      interface as a Layer2.
    type: str
    required: true
  admin_state:
    description: Admin State status of interface.
    default: 'up'
    choices: ['up', 'down']
    required: false
    type: str
  description:
    description: Description of interface.
    type: str
    required: false
  vlan_mode:
    description: VLAN mode on interface, access or trunk.
    choices: ['access', 'trunk']
    required: false
    type: str
  vlan_access:
    description: Access VLAN ID, vlan_mode must be set to access.
    required: false
    type: str
  vlan_trunks:
    description: List of trunk VLAN IDs, vlan_mode must be set to trunk.
    required: false
    type: list
  trunk_allowed_all:
    description: Flag for vlan trunk allowed all on L2 interface, vlan_mode
      must be set to trunk.
    required: false
    type: bool
  native_vlan_id:
    description: VLAN trunk native VLAN ID, vlan_mode must be set to trunk.
    required: false
    type: str
  native_vlan_tag:
    description: Flag for accepting only tagged packets on VLAN trunk native,
      vlan_mode must be set to trunk.
    required: false
    type: bool
  interface_qos_schedule_profile:
    description: Attaching existing QoS schedule profile to interface.
    type: dict
    required: False
  interface_qos_rate:
    description: "The rate limit value configured for
      broadcast/multicast/unknown unicast traffic. Dictionary should have the
      format ['type_of_traffic'] = speed i.e. {'unknown-unicast': 100pps,
      'broadcast': 200pps, 'multicast': 200pps}"
    type: dict
    required: False
  state:
    description: Create, Update, or Delete Layer2 Interface
    choices: ['create', 'delete', 'update']
    default: 'create'
    required: false
    type: str
'''  # NOQA

EXAMPLES = '''
- name: Configure Interface 1/1/3 - vlan trunk allowed all
  aoscx_l2_interface:
    interface: 1/1/3
    vlan_mode: trunk
    trunk_allowed_all: True

- name: Delete Interface 1/1/3
  aoscx_l2_interface:
    interface: 1/1/3
    state: delete

- name: Configure Interface 1/1/1 - vlan trunk allowed 200
  aoscx_l2_interface:
    interface: 1/1/1
    vlan_mode: trunk
    vlan_trunks: '200'

- name: Configure Interface 1/1/1 - vlan trunk allowed 200,300
  aoscx_l2_interface:
    interface: 1/1/1
    vlan_mode: trunk
    vlan_trunks: ['200','300']

- name: Configure Interface 1/1/1 - vlan trunk allowed 200,300 , vlan trunk native 200
  aoscx_l2_interface:
    interface: 1/1/3
    vlan_mode: trunk
    vlan_trunks: ['200','300']
    native_vlan_id: '200'

- name: Configure Interface 1/1/4 - vlan access 200
  aoscx_l2_interface:
    interface: 1/1/4
    vlan_mode: access
    vlan_access: '200'

- name: Configure Interface 1/1/5 - vlan trunk allowed all, vlan trunk native 200 tag
  aoscx_l2_interface:
    interface: 1/1/5
    vlan_mode: trunk
    trunk_allowed_all: True
    native_vlan_id: '200'
    native_vlan_tag: True

- name: Configure Interface 1/1/6 - vlan trunk allowed all, vlan trunk native 200
  aoscx_l2_interface:
    interface: 1/1/6
    vlan_mode: trunk
    trunk_allowed_all: True
    native_vlan_id: '200'
'''  # NOQA

RETURN = r''' # '''

from ansible.module_utils.aoscx_vlan import VLAN
from ansible.module_utils.aoscx_interface import L2_Interface, Interface
from ansible.module_utils.aoscx import ArubaAnsibleModule

def main():
    module_args = dict(
        interface=dict(type='str', required=True),
        admin_state=dict(type='str', default='up', choices=['up', 'down']),
        description=dict(type='str', default=None),
        vlan_mode=dict(type='str', default=None, choices=['access', 'trunk']),
        vlan_access=dict(type='str', default=None),
        vlan_trunks=dict(type='list', default=None),
        trunk_allowed_all=dict(type='bool', default=None),
        native_vlan_id=dict(type='str', default=None),
        native_vlan_tag=dict(type='bool', default=None),
        interface_qos_schedule_profile=dict(type='dict', default=None),
        interface_qos_rate=dict(type='dict', default=None),
        state=dict(type='str', default='create',
                   choices=['create', 'delete', 'update'])
    )

    # Version management
    try:
        from ansible.module_utils.aoscx_pyaoscx import Session
        from pyaoscx.session import Session as Pyaoscx_Session
        from pyaoscx.pyaoscx_factory import PyaoscxFactory

        USE_PYAOSCX_SDK = True

    except ImportError:

        USE_PYAOSCX_SDK = False

    if USE_PYAOSCX_SDK:

        from ansible.module_utils.basic import AnsibleModule
        # ArubaModule
        ansible_module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True)

        interface_name = ansible_module.params['interface']
        admin_state = ansible_module.params['admin_state']
        # Set all variables
        description = ansible_module.params['description']
        vlan_mode = ansible_module.params['vlan_mode']
        vlan_access = ansible_module.params['vlan_access']
        vlan_trunks = ansible_module.params['vlan_trunks']
        trunk_allowed_all = ansible_module.params['trunk_allowed_all']
        native_vlan_id = ansible_module.params['native_vlan_id']
        native_vlan_tag = ansible_module.params['native_vlan_tag']
        qos_profile_details = ansible_module.params['interface_qos_schedule_profile']
        qos_rate = ansible_module.params['interface_qos_rate']
        state = ansible_module.params['state']

        # Session
        session = Session(ansible_module)

        # Set result var
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

        if state == 'delete':
            # Create Interface Object
            interface = pyaoscx_factory.interface(interface_name)
            # Delete it
            interface.delete()

            # Changed
            result['changed'] = True

        if state == 'create' or state == 'update':
            # Set VLAN tag
            vlan_tag = None
            if vlan_access is not None:
                vlan_tag = vlan_access
            elif native_vlan_id is not None:
                vlan_tag = native_vlan_id

            if isinstance(vlan_tag, str):
                vlan_tag = int(vlan_tag)

            # Create Interface Object
            interface = pyaoscx_factory.interface(interface_name)
            # Verify if interface was create
            if interface.was_modified():
                # Changed
                result['changed'] = True
            # Configure L2
            # Verify if object was changed
            modified_op = interface.configure_l2(
                description=description,
                admin=admin_state,
                vlan_mode=vlan_mode,
                vlan_tag=vlan_tag,
                vlan_ids_list=vlan_trunks,
                trunk_allowed_all=trunk_allowed_all,
                native_vlan_tag=native_vlan_tag)

            if qos_profile_details is not None:
                modified_op2 = interface.update_interface_qos_profile(
                    qos_profile_details)
                modified_op = modified_op2 or modified_op

            if qos_rate is not None:
                modified_op3 = interface.update_interface_qos_rate(qos_rate)
                modified_op = modified_op3 or modified_op

            if modified_op:
                # Changed
                result['changed'] = True
        # Exit
        ansible_module.exit_json(**result)
    else:

        aruba_ansible_module = ArubaAnsibleModule(module_args)

        params = {}
        for param in aruba_ansible_module.module.params.keys():
            params[param] = aruba_ansible_module.module.params[param]

        state = aruba_ansible_module.module.params['state']
        admin_state = aruba_ansible_module.module.params['admin_state']
        interface_name = aruba_ansible_module.module.params['interface']
        description = aruba_ansible_module.module.params['description']
        interface_qos_rate = aruba_ansible_module.module.params[
            'interface_qos_rate']
        interface_qos_schedule_profile = aruba_ansible_module.module.params[
            'interface_qos_schedule_profile']

        l2_interface = L2_Interface()
        interface = Interface()
        vlan = VLAN()

        interface_vlan_dict = {}

        if params['state'] == 'create':
            aruba_ansible_module = l2_interface.create_l2_interface(
                aruba_ansible_module, interface_name)

            if params['vlan_mode'] == 'access':
                interface_vlan_dict['vlan_mode'] = 'access'

                if params['vlan_access'] is None:
                    interface_vlan_dict['vlan_tag'] = 1

                elif vlan.check_vlan_exist(aruba_ansible_module,
                                           params['vlan_access']):
                    interface_vlan_dict['vlan_tag'] = params['vlan_access']

                else:
                    aruba_ansible_module.module.fail_json(
                      msg="VLAN {id} is not "
                      "configured"
                      "".format(
                          id=params['vlan_access']))  # NOQA

            elif params['vlan_mode'] == 'trunk':

                if params['native_vlan_id']:
                    if params['native_vlan_id'] == '1':
                        interface_vlan_dict['vlan_tag'] = '1'
                        if params['native_vlan_tag']:
                            interface_vlan_dict['vlan_mode'] = 'native-tagged'
                        else:
                            interface_vlan_dict['vlan_mode'] = 'native-untagged'
                    elif vlan.check_vlan_exist(aruba_ansible_module,
                                               params['native_vlan_id']):
                        if params['native_vlan_tag']:
                            interface_vlan_dict['vlan_mode'] = 'native-tagged'
                        else:
                            interface_vlan_dict['vlan_mode'] = 'native-untagged'
                        interface_vlan_dict['vlan_tag'] = params['native_vlan_id']
                    else:
                        aruba_ansible_module.module.fail_json(
                            msg="VLAN {id} is not configured".format(
                                id=params['native_vlan_id']))

                elif params['native_vlan_tag']:
                    interface_vlan_dict['vlan_mode'] = 'native-tagged'
                    interface_vlan_dict['vlan_tag'] = '1'

                else:
                    interface_vlan_dict['vlan_mode'] = 'native-untagged'
                    interface_vlan_dict['vlan_tag'] = '1'

                if not params['trunk_allowed_all'] and params['vlan_trunks']:
                    if 'vlan_mode' not in interface_vlan_dict.keys():
                        interface_vlan_dict['vlan_mode'] = 'native-untagged'
                    interface_vlan_dict['vlan_trunks'] = []
                    for id in params['vlan_trunks']:
                        if vlan.check_vlan_exist(aruba_ansible_module, id):
                            interface_vlan_dict['vlan_trunks'].append(str(id))
                        else:
                            aruba_ansible_module.module.fail_json(
                                msg="VLAN {id} is not configured".format(id=id))

                elif params['trunk_allowed_all']:
                    if 'vlan_mode' not in interface_vlan_dict.keys():
                        interface_vlan_dict['vlan_mode'] = 'native-untagged'

            else:
                interface_vlan_dict['vlan_mode'] = 'access'
                interface_vlan_dict['vlan_tag'] = 1

            aruba_ansible_module = l2_interface.update_interface_vlan_details(
                aruba_ansible_module, interface_name, interface_vlan_dict)

        if state == 'delete':
            aruba_ansible_module = l2_interface.delete_l2_interface(
                aruba_ansible_module, interface_name)

        if (state == 'update') or (state == 'create'):

            if admin_state is not None:
                aruba_ansible_module = interface.update_interface_admin_state(
                    aruba_ansible_module, interface_name, admin_state)

            if description is not None:
                aruba_ansible_module = interface.update_interface_description(
                    aruba_ansible_module, interface_name, description)

            if interface_qos_rate is not None:
                aruba_ansible_module = l2_interface.update_interface_qos_rate(
                    aruba_ansible_module, interface_name, interface_qos_rate)

            if interface_qos_schedule_profile is not None:
                aruba_ansible_module = l2_interface.update_interface_qos_profile(
                    aruba_ansible_module, interface_name, interface_qos_schedule_profile)

        aruba_ansible_module.update_switch_config()


if __name__ == '__main__':
    main()
