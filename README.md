
aoscx
=========

This Ansible network role provides a set of platform-dependent configuration
 management modules specifically designed for the AOS-CX network device.

Requirements
------------

* Python 3 or later
* Ansible 2.8.1 or later  
  * Refer to [Ansible's documentation](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) for installation steps
  * Ansible 2.10+ requires `ansible.netcommon` collection to be installed  
* Minimum supported AOS-CX firmware version 10.04.
* Enable REST on your AOS-CX device with the following commands:
    ```
    switch(config)# https-server rest access-mode read-write
    switch(config)# https-server vrf mgmt
    ```

Installation
------------

Through Galaxy:
```
ansible-galaxy install arubanetworks.aoscx_role
```

Example Output:
```
Starting galaxy role install process
- downloading role 'aoscx_role', owned by arubanetworks
- downloading role from https://github.com/aruba/aoscx-ansible-role/archive/3.0.1.tar.gz
- extracting arubanetworks.aoscx_role to /users/chiapuzi/.ansible/roles/arubanetworks.aoscx_role
- arubanetworks.aoscx_role (3.0.1) was installed successfully
ansible-control-machine$
```

* **Change into the roles directory** where the Ansible role was installed, execute `ansible-galaxy role list` to find:
	```
	ansible-control-machine$ansible-galaxy role list
	# /users/chiapuzi/.ansible/roles
	- arubanetworks.aoscx_role, 3.0.1
	- arubanetworks.aruba_central_role, 0.1.0
	[WARNING]: - the configured path /usr/share/ansible/roles does not exist.
	[WARNING]: - the configured path /etc/ansible/roles does not exist.
	ansible-control-machine$cd /users/chiapuzi/.ansible/roles/arubanetworks.aoscx_role/
	ansible-control-machine$ls
	cliconf_plugins     httpapi_plugins  README.md         terminal_plugins
	connection_plugins  library          RELEASE-NOTES.md
	CONTRIBUTING.md     meta             requirements.txt
	docs                module_utils     requirements.yml
	ansible-control-machine$
	```

	* Install all Ansible requirements, with the following command:
	    ```
	    ansible-galaxy install -r requirements.yml
	    ```
	* Install all Python requirements with the following command:
	    ```
	    python3 -m pip install -r requirements.txt
	    ```
* **Change back** into your working directory and begin automating!
	```
	ansible-control-machine$cd /users/chiapuzi/Desktop/sandbox/
	```

SSH/CLI Modules
---------------
* To use the SSH/CLI modules `aoscx_config` and `aoscx_command`, SSH access must
 be enabled on your AOS-CX device. It is enabled by default.
    * If necessary, re-enable SSH access on the device with the following command:
    ```
    switch(config)# ssh server vrf mgmt
    ```
* The control machine's `known_hosts` file must contain the target device's public key.
    * Alternatively, host key checking by the control machine may be disabled, although this is not recommended.
    * To disable host key checking modify the ansible.cfg file (default /etc/ansible/ansible.cfg) to include:
      `host_key_checking = false`
  
#### Limitations and Notes
* The default command timeout is 30 seconds. If a command takes more than 30
 seconds to execute, the task will time out.
	* If you regularly encounter the `command timeout triggered, timeout value
	 is 30 secs` error, consider setting the environment variable 
	`ANSIBLE_PERSISTENT_COMMAND_TIMEOUT` to a greater value. See Ansible documentation [here](https://docs.ansible.com/ansible/latest/network/user_guide/network_debug_troubleshooting.html).


Inventory Variables
-------------------

The variables that should be defined in your inventory for your AOS-CX host are:

* `ansible_host`: IP address of switch in `A.B.C.D` format. For IPv6 hosts use a string and enclose in square brackets E.G. `'[2001::1]'`.
* `ansible_user`: Username for switch in `plaintext` format  
* `ansible_password`: Password for switch in `plaintext` format
* `ansible_network_os`: Must always be set to `aoscx`
* `ansible_connection`: Set to `httpapi` to use REST API modules, to `network_cli` to use SSH/CLI modules and to `aoscx` to use pyaoscx modules
  * See [below](#pyaoscx-modules) for info on our new pyaoscx implementation of the AOS-CX Ansible modules that will be the standard moving forward
  * See [below](#using-both-rest-api-and-sshcli-modules-on-a-host) for info on using both REST API modules and SSH/CLI modules on a host
* `ansible_httpapi_use_ssl`: (Only required for REST API modules) Must always be `True` as AOS-CX uses port 443 for REST
* `ansible_httpapi_validate_certs`: (Only required for REST API modules) Set `True` or `False` depending on if Ansible should attempt to validate certificates
* `ansible_acx_no_proxy`: Set to `True` or `False` depending if Ansible should bypass environment proxies to connect to AOS-CX
* `ansible_aoscx_validate_certs`: Set to `True` or `False` depending if Ansible should bypass validating certificates to connect to AOS-CX. Only required when `ansible_connection` is set to `aoscx`
* `ansible_aoscx_use_proxy`: Set to `True` or `False` depending if Ansible should bypass environment proxies to connect to AOS-CX. Only required when `ansible_connection` is set to `aoscx`.



pyaoscx Modules
---------------
In an effort to make use of our recently updated Python SDK for AOS-CX [Pyaoscx](https://pypi.org/project/pyaoscx/) we've redesigned our Ansible integration by making use of pyaoscx for all REST-API based modules.   
**What does this mean if I've been using Ansible with AOS-CX REST API modules?**   
Our previous implementation will continue to function but will not be supported for future modules. That means you should and eventually have to update your [Ansible Inventory variables](https://github.com/aruba/aoscx-ansible-role#pyaoscx-modules-only) to specify the `ansible_network_os=aoscx` and additional variables as well as install the pyaoscx Python package using Python3 pip, **all playbooks will remain the same**:   
`pip3 install pyaoscx`  
The AOS-CX Ansible Role will automatically determine if you have pyaoscx installed and will use that method when the `ansible_network_os` is set to `aoscx`. If it's set to `httpapi` it will continue to use the previous implementation method.    

### Sample Inventories:

#### REST API Modules Only:

##### INI

```INI
aoscx_1 ansible_host=10.0.0.1 ansible_user=admin ansible_password=password ansible_network_os=aoscx ansible_connection=aoscx ansible_aoscx_validate_certs=False ansible_aoscx_use_proxy=False
```

##### YAML

```yaml
all:
  hosts:
    aoscx_1:
      ansible_host: 10.0.0.1
      ansible_user: admin
      ansible_password: password
      ansible_network_os: aoscx
      ansible_connection: aoscx  # REST API via pyaoscx connection method
      ansible_aoscx_validate_certs: False
      ansible_aoscx_use_proxy: False
      ansible_acx_no_proxy: True
```


#### Legacy REST API Modules:

##### INI

```INI
aoscx_1 ansible_host=10.0.0.1 ansible_user=admin ansible_password=password ansible_network_os=aoscx ansible_connection=httpapi ansible_httpapi_validate_certs=False ansible_httpapi_use_ssl=True ansible_acx_no_proxy=True
```

##### YAML


```yaml
all:
  hosts:
    aoscx_1:
      ansible_host: 10.0.0.1
      ansible_user: admin
      ansible_password: password
      ansible_network_os: aoscx
      ansible_connection: httpapi  # REST API connection method
      ansible_httpapi_validate_certs: False
      ansible_httpapi_use_ssl: True
      ansible_acx_no_proxy: True
```

#### SSH/CLI Modules Only:

##### INI

```INI
aoscx_1 ansible_host=10.0.0.1 ansible_user=admin ansible_password=password ansible_network_os=aoscx ansible_connection=network_cli
```

##### YAML

```yaml
all:
  hosts:
    aoscx_1:
      ansible_host: 10.0.0.1
      ansible_user: admin
      ansible_password: password
      ansible_network_os: aoscx
      ansible_connection: network_cli  # SSH connection method
```

Example Playbooks
-----------------

### Including the Role

If role installed through Galaxy add `arubanetworks.aoscx_role` to your list of roles:

```yaml
- hosts: all
  roles:
    - role: arubanetworks.aoscx_role
  vars:
    ansible_python_interpreter: /usr/bin/python3
  gather_facts: False     
  tasks:
  - name: Create L3 Interface 1/1/3
    aoscx_l3_interface:
      interface: 1/1/3
      description: Uplink_Interface
      ipv4: ['10.20.1.3/24']
      ipv6: ['2001:db8::1234/64']
```

Using Both REST API and SSH/CLI Modules on a Host
-------------------------------------------------

To use both REST API and SSH/CLI modules on the same host, 
you must create separate plays such 
that each play uses either only REST API modules or only SSH/CLI modules.
A play cannot mix and match REST API and SSH/CLI module calls.
In each play, `ansible_connection` must possess the appropriate value 
according to the modules used. 
If the play uses REST API modules, the value should be `aoscx`. 
If the play uses SSH/CLI modules, the value should be `network_cli`.
 
A recommended approach to successfully using both types of modules for a host
is as follows:
1. Set the host variables such that Ansible will connect to the host using REST API,
like seen [above](#rest-api-modules-only).
2. In the playbook, in each play wherein the SSH/CLI
modules are used, set the `ansible_connection` to `network_cli`. 

The inventory should look something like this:

```yaml
all:
  hosts:
    aoscx_1:
      ansible_host: 10.0.0.1
      ansible_user: admin
      ansible_password: password
      ansible_network_os: aoscx
      ansible_connection: aoscx  # REST API connection method
      ansible_httpapi_validate_certs: False
      ansible_httpapi_use_ssl: True
      ansible_acx_no_proxy: True
```

and the playbook like this (note how the second play, which uses the SSH/CLI module `aoscx_command`,
sets the `ansible_connection` value accordingly):

```yaml
- hosts: all
  roles: 
    - role: arubanetworks.aoscx_role
  vars:
     ansible_python_interpreter: /usr/bin/python3
  gather_facts: False     
  tasks:
  - name: Adding or Updating Banner
    aoscx_banner:
      banner_type: banner
      banner: "Hi!"

- hosts: all
  roles: 
    - role: arubanetworks.aoscx_role
  vars:
    ansible_connection: network_cli
  gather_facts: False    
  tasks:
    - name: Execute show run on the switch
      aoscx_command:
        commands: ['show run']
```


Contribution
-------
At Aruba Networks we're dedicated to ensuring the quality of our products, so if you find any
issues at all please open an issue on our [Github](https://github.com/aruba/aoscx-ansible-role) and we'll be sure to respond promptly!

For more contribution opportunities follow our guidelines outlined in our [CONTRIBUTING.md](https://github.com/aruba/aoscx-ansible-role/blob/master/CONTRIBUTING.md)

License
-------

Apache 2.0

Author Information
------------------
 - Madhusudan Pranav Venugopal (@madhusudan-pranav-venugopal)
 - Yang Liu (@yliu-aruba)
 - Tiffany Chiapuzio-Wong (@tchiapuziowong)
 - Derek Wang (@derekwangHPEAruba)
 - Daniel Alvarado Bonilla (@daniel-alvarado)

