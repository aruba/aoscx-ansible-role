#!/usr/bin/python
# -*- coding: utf-8 -*-

# (C) Copyright 2022 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "certified",
}

DOCUMENTATION = """
---
module: aoscx_qos
version_added: "2.8"
short_description: Create or Delete QoS Schedule Profiles on AOS-CX
description: >
  This module provides configuration management of QoS Schedule Profiles on
  AOS-CX devices.
author: Aruba Networks (@ArubaNetworks)
options:
  name:
    description: The Schedule Profile name.
    required: true
    type: str
  vsx_sync:
    description: Attributes to be synchronized between VSX peers.
    required: false
    type: list
    choices:
      - all_attributes_and_dependents
  state:
    description: Create, update, or delete a Schedule Profile.
    required: false
    choices:
      - create
      - update
      - delete
    default: create
    type: str
"""

EXAMPLES = """
---
- name: Create Schedule Profile named "High-Traffic"
  aoscx_qos:
    name: High-Traffic
    state: create

- name: Delete Schedule Profile named "Low-Traffic"
  aoscx_qos:
    name: Low-Traffic
    state: delete

- name: Update a Schedule Profile named "Medium-Traffic"; set its vsx_sync
  aoscx_qos:
    name: Medium-Traffic
    vsx_sync:
      - all_attributes_and_dependents
    state: update

- name: Create Schedule Profile 'Medium-Traffic'
  aoscx_qos:
    name: Medium-Traffic
    state: update

- name: >
    Set the switch's global Schedule Profile to a Schedule Profile named
    Medium-Traffic
  aoscx_system:
    global_schedule_profile: Medium-Traffic
"""

RETURN = r""" # """

try:
    from pyaoscx.device import Device
except ImportError as imp:
    raise ImportError(
        "Unable to find the PYAOSCX SDK. Make sure it is installed correctly."
    ) from imp

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.aoscx_pyaoscx import (
    get_pyaoscx_session,
)
from ansible.module_utils.aoscx import (
    aoscx_http_argument_spec,
)


def get_argument_spec():
    argument_spec = {
        "name": {
            "type": "str",
            "required": True,
        },
        "state": {
            "type": "str",
            "default": "create",
            "choices": ["create", "update", "delete"],
        },
        "vsx_sync": {
            "type": "list",
            "required": False,
            "choices": ["all_attributes_and_dependents"],
            "default": None,
        },
    }
    argument_spec.update(aoscx_http_argument_spec)
    return argument_spec


def main():
    ansible_module = AnsibleModule(
        argument_spec=get_argument_spec(),
        supports_check_mode=True,
    )

    result = dict(
        changed=False
    )

    if ansible_module.check_mode:
        ansible_module.exit_json(**result)

    session = get_pyaoscx_session(ansible_module)

    # Get playbook's arguments
    name = ansible_module.params["name"]
    state = ansible_module.params["state"]
    vsx_sync = ansible_module.params["vsx_sync"]

    device = Device(session)

    schedule_profile_kw = {}
    if vsx_sync:
        schedule_profile_kw["vsx_sync"] = vsx_sync

    if state == "delete":
        if not device.materialized:
            device.get()
        if device.qos_default == name:
            msg = (
                "Skipping, cannot delete Schedule Profile, while it is set "
                "as global."
            )
            result["msg"] = msg
            result["skipped"] = True
        else:
            sched_profile = device.qos(name)
            result["changed"] = sched_profile.was_modified()
            sched_profile.delete()
            # only report deletion if object existed before call to ansible
            result["changed"] = not result["changed"]
    else:
        sched_profile = device.qos(name, **schedule_profile_kw)
        result["changed"] = sched_profile.was_modified()

    # Exit
    ansible_module.exit_json(**result)


if __name__ == "__main__":
    main()
