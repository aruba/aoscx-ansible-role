#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (C) Copyright 2019 Hewlett Packard Enterprise Development LP.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'certified'
}

DOCUMENTATION = '''
---
module: aoscx_vrf_interface
version_added: "2.8"
short_description: Create or Delete VRF attach configuration on Interfaces on AOS-CX
description:
  - This modules provides configuration management of VRF attachment on
    interfaces on AOS-CX devices.
author:
  - Aruba Networks
options:
  vrf_name:
    description: The name of the VRF to be attached to Interface
    required: true
  interface_list:
    description: List of interfaces being added or removed from the VRF.
    required: true
  state:
    description: Create or delete the interfaces from the VRF. If an interface
      is already attached to a VRF (default or user created) and a user wants
      to change the VRF the interface is attached to, the user must delete the
      instance of the Interface from the configuration then recreate with the
      desired VRF.
    required: false
    choices: ['create', 'delete', 'update']
    default: create
'''  # NOQA

EXAMPLES = '''
- name: Create a VRF interface
    aoscx_vrf_interface:
        vrf_name: vrf2
        interface_list: ['1/1/2', '1/1/3']
        state: "create"

- name: Delete a VRF interface
    aoscx_vrf_interface:
        vrf_name: vrf2
        interface_list: ['1/1/2', '1/1/3']
        state: delete
'''

RETURN = r''' # '''

from ansible.module_utils.aoscx import ArubaAnsibleModule
from ansible.module_utils.aoscx_interface import L3_Interface


def main():
    module_args = dict(
        vrf_name=dict(type='str', default='default'),
        interface_list=dict(type='list', required=True),
        state=dict(default='create', choices=['create', 'delete', 'update'])
    )

    aruba_ansible_module = ArubaAnsibleModule(module_args)

    vrf_name = aruba_ansible_module.module.params['vrf_name']
    vrf_interface_list = aruba_ansible_module.module.params['interface_list']
    state = aruba_ansible_module.module.params['state']

    l3_interface = L3_Interface()

    if state == 'create' or state == 'update':
        update_type = 'insert'
    else:
        update_type = 'delete'

    for interface_name in vrf_interface_list:
        error = ("Interface {} is configured as L2 or L3 interface in VRF\n"
                 "Delete interface from configuration then recreate with "
                 "desired VRF".format(interface_name))
        if not l3_interface.check_if_l3_interface_possible(aruba_ansible_module, interface_name):  # NOQA
            aruba_ansible_module.module.fail_json(msg=error)

        aruba_ansible_module = l3_interface.update_interface_vrf_details_from_vrf(aruba_ansible_module, vrf_name, interface_name, update_type)  # NOQA

    aruba_ansible_module.update_switch_config()


if __name__ == '__main__':
    main()
