
################################################################################
#                                                                              #
# Copyright (c) 2021 Cisco Systems                                             #
# All Rights Reserved.                                                         #
#                                                                              #
#    Licensed under the Apache License, Version 2.0 (the "License"); you may   #
#    not use this file except in compliance with the License. You may obtain   #
#    a copy of the License at                                                  #
#                                                                              #
#         http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                              #
#    Unless required by applicable law or agreed to in writing, software       #
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT #
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the  #
#    License for the specific language governing permissions and limitations   #
#    under the License.                                                        #
#                                                                              #
################################################################################

from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.fabric.FabricVlan import FabricVlan
from ucsmsdk.mometa.fabric.FabricNetGroup import FabricNetGroup
from ucsmsdk.mometa.fabric.FabricPooledVlan import FabricPooledVlan
from ucsmsdk.mometa.fabric.FabricNetGroupRef import FabricNetGroupRef
import vars
import argparse
import os
import logging
import urllib3
import getpass
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


if __name__ == "__main__":

    # Get command line arguments
    parser = argparse.ArgumentParser(description="Create/Delete VLAN Group in UCS")
    parser.add_argument('-i_vlan', '--initial_vlan', required=True)
    parser.add_argument('-e_vlan', '--ending_vlan', required=True)
    parser.add_argument('-np', '--name_prefix', required=True)
    parser.add_argument('-vnic', '--vnic_name', required=True)
    parser.add_argument('-vgrp', '--vlan_group_name', required=True)
    parser.add_argument('-d', '--delete', default=False, action="store_true")
    args = parser.parse_args()

    initial_vlan = args.initial_vlan
    ending_vlan = args.ending_vlan
    vlan_name_prefix = args.name_prefix
    vnic_name = args.vnic_name
    vlan_group_name = args.vlan_group_name

    # Get USCM  Credentials
    ucs_passwordd = getpass.getpass('UCS Password:')

    # Create logger object
    logging.basicConfig(level=logging.INFO)
    logfh = logging.FileHandler(os.path.join('./', 'ucs_aci_vlan.log'))
    logger = logging.getLogger('ucs_aci_vlan')
    logger.addHandler(logfh)
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logfh.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)

    # Login to UCS Manager
    handle = UcsHandle(vars.UCS_IP_ADDRESS, vars.UCS_USERNAME, ucs_passwordd)
    handle.login()

    # Create/Delete VLAN Group
    vlan_group_mo = FabricNetGroup(parent_mo_or_dn="fabric/lan", name=vlan_group_name)
    if args.delete:
        handle.remove_mo(vlan_group_mo)
    else:
        handle.add_mo(vlan_group_mo)
    try:
        handle.commit()
        logger.debug(f"Creating VLAN Group {vlan_group_name}")
    except Exception as e:
        logger.error(f"{e} - Creating VLAN Group {vlan_group_name}")

    # Create/Delete VLAN MOs add to VLAN Group
    for vlan_id in range(int(initial_vlan), int(ending_vlan) + 1):
        vlan_mo = FabricVlan(parent_mo_or_dn='fabric/lan', name=f"{vlan_name_prefix}-{vlan_id}", id=str(vlan_id))
        vlan_to_group_mo = FabricPooledVlan(parent_mo_or_dn=vlan_group_mo, name=f"{vlan_name_prefix}-{vlan_id}")
        if args.delete:
            handle.remove_mo(vlan_mo)
        else:
            handle.add_mo(vlan_mo)
            handle.add_mo(vlan_to_group_mo)

        try:
            handle.commit()
            logger.debug("Creating VLAN {}".format(vlan_id))
        except Exception as e :
            logger.error("{} - Create VLAN {}".format(e, vlan_id))

    # GET vNIC MO
    vnic_mo = None
    vnic_mos = handle.query_classid("VnicLanConnTempl")
    for vnic in vnic_mos:
        if vnic.name == vnic_name:
            vnic_mo = vnic

    if vnic_mo is None:
        logger.error("vNIC {} not found".format(vnic_name))
        exit(0)

    # Trunk VLANs on vNIC using VLAN Group
    vlan_group_vnic_mo = FabricNetGroupRef(parent_mo_or_dn=vnic_mo, name=vlan_group_name)
    if args.delete:
        handle.remove_mo(vlan_group_vnic_mo)
    else:
        handle.add_mo(vlan_group_vnic_mo)

    try:
        handle.commit()
        logger.debug("Assigning VLAN Group {} to vNIC template {}".format(vlan_group_name, vnic_name))
    except Exception as e :
        logger.error("{} - Assing VLAN Group {} to vNIC template {}".format(e, vlan_group_name, vnic_name))

    handle.logout()
