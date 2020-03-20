#!/usr/bin/python
# -*- coding: utf-8 -*-

# (C) Copyright 2020 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

class FactsArgs(object):
    """ The arg spec for the aoscx facts module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        'gather_subset': dict(default=['!config'], type='list'),
        'gather_network_resources': dict(type='list'),
    }