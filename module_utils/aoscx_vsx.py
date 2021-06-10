#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (C) Copyright 2020 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    from pyaoscx import vsx, interface
    HAS_PYAOSCX = True
except ImportError:
    HAS_PYAOSCX = False


def create_vsx(role, isl_port, keepalive_interface, keepalive_peer, keepalive_src, keepalive_vrf, vsx_mac, **session):
    result = dict(
        changed=False
    )
    vsx_config = vsx.get_vsx(selector="configuration", **session)
    if not vsx_config:
        # no vsx config found proceed with creation
        result["changed"] = vsx.create_vsx(role, isl_port, keepalive_peer, keepalive_src, keepalive_vrf, vsx_mac, **session)
    return result


def delete_vsx(**session):
    result = dict(
        changed=False
    )
    vsx_config = vsx.get_vsx(selector="configuration", **session)
    if vsx_config:
        # vsx config found proceed with deletion
        result["changed"] = vsx.delete_vsx(**session)
    return result
