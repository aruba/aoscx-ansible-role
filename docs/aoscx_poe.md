# Power over Ethernet

Power over Ethernet module for Ansible.

Version added: 2.8

 - [Synopsis](#Synopsis)
 - [Parameters](#Parameters)
 - [Examples](#Examples)

## Synopsis

Power-over-ethernet (PoE) manages power supplied to devices using standard Ethernet data cables by managing an Interface's Configuration. You can find additional information online about how PoE is structured at the [Aruba Portal](https://developer.arubanetworks.com/aruba-aoscx/reference/get_system-interfaces-name-poe-interface)

## Parameters

| Parameter     | Type   | Choices/Defaults                 | Required | Comments                                                                                                                                                                                                   |
|:--------------|:------:|:--------------------------------:|:--------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `interface`   | string |                                  | [x]      | The name of an interface available inside a switch.                                                                                                                                                        |
| `enable`      | bool   |                                  | [ ]      | Configurable flag to control PoE power delivery on this Interface. A value of true would enable PoE power delivery on this Interface. By default, the flag is set to false for all PoE capable Interfaces. |
| `criticality` | string | [`low`, `high`, `critical`]      | [ ]      | Power criticality level for the PoE Interface.                                                                                                                                                             |

## Examples

### 1. Enable Power over Ethernet

The following example enables PoE on the '1/1/5' and '1/1/10' interfaces.

```YAML
- name: Enable Power over Ethernet on Interface '1/1/5'
  aoscx_poe:
    interface: 1/1/5
    enable: True

- name: Enable Power Over Ethernet on Interface '1/1/10'
  aoscx_poe:
    interface: 1/1/10
    enable: True
```

### 2. Disable Power over Ethernet

The following example disables PoE on the '1/1/7' interface.

```YAML
- name: Disable Power Over Ethernet on Interface '1/1/7'
  aoscx_poe:
    interface: 1/1/7
    enable: False
```

### 3. Set criticality levels

The following examples set different criticality levels to different interfaces.

```YAML
- name: Configure PoE on Interface '1/1/23'
  aoscx_poe:
    interface: 1/1/23
    criticality: low

- name: Configure and enable PoE on Interface '1/1/24'
  aoscx_poe:
    interface: 1/1/24
    enable: True
    criticality: high

- name: Configure PoE on Interface '1/1/25'
  aoscx_poe:
    interface: 1/1/25
    criticality: critical
```
