# azure-quick-attach
This script's purpose is to easily attach one or many data disks that were orophaned from a VM deletion.

## Prerequisities

You will need to have a json formatted output of your VM's details before deleting it. This can be easily gathered by using the [Azure Xplat CLI](https://github.com/Azure/azure-xplat-cli):

`azure vm show <resource_group> <vm_name> --json > vm.json`

This script is also built to run off Python 3.5.x

## Usage

1) Clone this repository to your local machine:

`git clone https://github.com/tamcclur/azure-quick-attach.git`

2) In the directory you will need to install some Azure Python modules:

`pip install -r requirements.txt`

3) Execute the script on a terminal with the following usage:

`./main.py <subscription_id> <resource_group> <vm_name> <path_to_json_file>`

Then watch as the script iterates through your json output and attachs your data disks in the same order and with the same caching options.
