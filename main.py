#!/usr/bin/env python

from azure.common.credentials import UserPassCredentials, ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.compute.models import VirtualMachine, HardwareProfile, StorageProfile, DataDisk, CachingTypes, VirtualHardDisk, DiskCreateOptionTypes
import msrest
import json
import argparse
import getpass
import sys
import os

class AttachDisks():
    """Main Class for attaching disks"""
    """This script will programmatically attach data disks to your VM from a .json file."""

    def __init__(self):
        parser = argparse.ArgumentParser(description='Will programmatically attach data disks to your VM from a .json file.')
        subscription_id = parser.add_argument('subscription_id', help='Input your account\'s subscription ID.')
        resource_group = parser.add_argument('resource_group', help='Input your VM\'s resourece group name.')
        vm_name = parser.add_argument('vm_name', help='Input your VM\'s name.')
        parser.add_argument('json_path', help='Path to VM\'s json output.')
        self.args = parser.parse_args()
        args = parser.parse_args()
        self.sub_id = args.subscription_id
        self.rg_name = args.resource_group
        self.vm_name = args.vm_name
        self.json_path = args.json_path
        self.login()

    def login(self):
        """Method to authenticate"""
        try:
            credentials = UserPassCredentials(
            userName,
            userPass
            )
            print('pass')
        except:
            print('Either your AD login/password is incorrect, or you are using an MFA. \n' +
            'MFA use with this script is not supported at this time')
            sys.exit(1)
        self.connecting_clients(credentials)

    def connecting_clients(self, credentials):
        # Defining Connecting Clients
        compute_client = ComputeManagementClient(credentials, self.sub_id)
        self.json_parse(compute_client)

    def json_parse(self, compute_client):
        """Parses the local .json file for previously attached disks"""
        with open(self.json_path) as fp:
            ingest = json.load(fp)
            for disk in ingest['storageProfile']['dataDisks']:
                result = compute_client.virtual_machines.create_or_update(
                    self.rg_name,
                    self.vm_name,
                    VirtualMachine(
                        location=ingest['location'],
                        storage_profile=StorageProfile(
                            data_disks=[DataDisk(
                                lun=disk['lun'],
                                caching=disk['caching'].lower(),
                                create_option=DiskCreateOptionTypes.attach,
                                name=disk['name'],
                                vhd=VirtualHardDisk(
                                    uri=disk['vhd']['uri']
                                    )
                                            )]
                                        )
                                    )
                                )
                print('Attaching disk {0} with name {1}, waiting until complete...'.format(disk['lun'], disk['name']))
                result.wait()
        print('All disks should be attached now.')

my_disks = AttachDisks()
