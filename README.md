# UCS-ACI VLAN Configuration


This Python script uses the [ucsmsdk](https://ucsmsdk.readthedocs.io/en/latest/) SDK to configure the UCS Manager

## Workflow

* Create VLAN Group
* Create VLANs, assign it them to the VLAN Group
* Asign VLAN Group to the vNIC 


## Execution
Enter in the `vars.py` file the UCS host information. Credentials are asked via cli
```
$ python3 python_create_vlan_apic_ucs.py -h
usage: python_create_vlan_apic_ucs.py [-h] -i_vlan INITIAL_VLAN -e_vlan
                                      ENDING_VLAN -np NAME_PREFIX -vnic
                                      VNIC_NAME -vgrp VLAN_GROUP_NAME [-d]

Create/Delete VLAN Group in UCS

optional arguments:
  -h, --help            show this help message and exit
  -i_vlan INITIAL_VLAN, --initial_vlan INITIAL_VLAN
  -e_vlan ENDING_VLAN, --ending_vlan ENDING_VLAN
  -np NAME_PREFIX, --name_prefix NAME_PREFIX
  -vnic VNIC_NAME, --vnic_name VNIC_NAME
  -vgrp VLAN_GROUP_NAME, --vlan_group_name VLAN_GROUP_NAME
  -d, --delete
```



```
$ python3 python_create_vlan_apic_ucs.py -i_vlan 1110 -e_vlan 1115 -np vlan -vnic TEST-vNIC -vgrp DVS_VLAN_GROUP
UCS Password:
DEBUG:ucs_aci_vlan:Creating VLAN Group DVS_VLAN_GROUP
DEBUG:ucs_aci_vlan:Creating VLAN 1110
DEBUG:ucs_aci_vlan:Creating VLAN 1111
DEBUG:ucs_aci_vlan:Creating VLAN 1112
DEBUG:ucs_aci_vlan:Creating VLAN 1113
DEBUG:ucs_aci_vlan:Creating VLAN 1114
DEBUG:ucs_aci_vlan:Creating VLAN 1115
DEBUG:ucs_aci_vlan:Assigning VLAN Group DVS_VLAN_GROUP to vNIC template TEST-vNIC
```