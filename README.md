# vCenter-Automation

This repository provides a Django application that automates the creation and updating of virtual machines (VMs) in VMware vCenter using Terraform. The application exposes a REST API for managing VMs, integrates with ManageEngine for ticketing, and uses Terraform for infrastructure as code.

## API Endpoints
### Create a VM
- URL: /api/v2/vcenter/create-machine/
- Method: POST
- Content-Type: application/json
- Sample Request:
```shell
curl --location '127.0.0.1:8000/api/v2/vcenter/create-machine/' \
--header 'Content-Type: application/json' \
--data '
{
    "datacenter": "Test",
    "cluster": "New Cluster",
    "datastore": "datastore1",
    "name": "Mr. Meeseeks",
    "cpu": 2,
    "ram": 2048,
    "disk_size": 40,
    "hostname": "Schwifty",
    "ip_addr": "172.24.22.6",
    "cidr": 29,
    "defaultGW": "172.22.24.1",
    "vlan_id": 0,
    "ticket_id": 137727
}'
```
### Update a VM 
- URL: /api/v2/vcenter/create-machine/
- Method: PUT
- Content-Type: application/json
- Sample Request:
```shell
curl --location --request PUT '127.0.0.1:8000/api/v2/vcenter/edit-machine/exampleVm/' \
--header 'Content-Type: application/json' \
--data '
{
    "cpu": 4,
    "ram": 4096,
    "ticket_id": 13772775
}'
```
