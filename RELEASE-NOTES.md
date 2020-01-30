# 2.0.0

## Notable Changes
* New Modules including 10.4 Module Compatibility Fixes
* This release includes new modules that allow for configuration management, firmware uploading, and system booting. Refer to module documentation found in [docs/](https://github.com/aruba/aoscx-ansible-role/tree/master/docs).

## New Modules
* aoscx_backup_config - This module downloads the configuration from the switch. It can also download the configuration to a remote TFTP server.
* aoscx_boot_firmware - This module boots the switch with the image present in the mentioned partition.
* aoscx_checkpoint - This module creates a new checkpoint or copies a config from the checkpoint.
* aoscx_upload_config - This module uploads a configuration onto the switch. It can also upload the configuration from a remote TFTP server.
* aoscx_upload_firmware - This module uploads a firmware onto the switch. It can also upload the firmware from HTTP server.

## Known Issues
* There is a known issue with the following modules on all platforms and 10.4 firmware version. Please only use these modules with 10.3 at this time: 
    * aoscx_l3_interface
    * aoscx_vlan_interface
* To upload firmware using HTTP server with the module aoscx_upload_firmware, the device must be running firmware version 10.4 or higher.

# 1.0.5

## Notable Changes
* 2.9 Fixes and formatting changes
* This allows the modules to be compatible with 2.9 and the formatting to be compliant with ansible-sanity.

# 1.0.4

## Notable Changes
* Bug Fixes L2 Interface
* fixes bugs with l2_interface module and trunk vlans

# 1.0.3

## Notable Changes
* Minor Bug Fixes

# 1.0.2

## Notable Changes
* Minor Bug Fixes
* Modifies modules to fix error messages and bugs with L3 interfaces and VRFs.

# 1.0.1

## Notable Changes
* It has a few fixes for ansible-lint warnings. It also fixes the role name in example playbook in the README.

# 1.0.0

## Notable Changes
* This is the initial release for the AOS-CX Ansible Role.
* For this release, only 10.3 AOS-CX firmware version is supported.