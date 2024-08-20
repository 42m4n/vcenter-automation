locals {
  templatevars = {
  }
}
#===============================================================================
# vSphere Data
#===============================================================================

data "vsphere_datacenter" "dc" {
  name = var.datacenter
}

data "vsphere_compute_cluster" "cluster" {
  name          = var.cluster
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_datastore" "datastore" {
  name          = var.datastore
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_host" "my_esxi_host" {
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_virtual_machine" "template-ubuntu22" {
  name          = var.template-name
  datacenter_id = data.vsphere_datacenter.dc.id
}
#===============================================================================
# vSphere Resources
#===============================================================================

resource "vsphere_host_port_group" "PortGroup" {
  host_system_id = data.vsphere_host.my_esxi_host.id
  virtual_switch_name = "vSwitch0"
  name = var.name
  vlan_id = var.vlan_id
  provisioner "local-exec" {
    command = "sleep 20"
  }
}
data "vsphere_network" "created_net" {
  depends_on = [ vsphere_host_port_group.PortGroup ]
  name = var.name
  datacenter_id = data.vsphere_datacenter.dc.id
}
resource "vsphere_virtual_machine" "standalone" {
  name                         = var.name
  resource_pool_id             = data.vsphere_compute_cluster.cluster.resource_pool_id
  datastore_id                 = data.vsphere_datastore.datastore.id
  wait_for_guest_net_timeout   = 0
  wait_for_guest_ip_timeout    = 0
  num_cpus                     = var.cpu
  num_cores_per_socket         = var.cpu
  memory                       = var.ram
  memory_reservation           = var.ram
  guest_id                     = data.vsphere_virtual_machine.template-ubuntu22.guest_id
  folder                       = "terraform"
  extra_config_reboot_required = true
  cpu_hot_add_enabled          = true
  host_system_id               = data.vsphere_host.my_esxi_host.id

  network_interface {
    network_id   = data.vsphere_network.created_net.id
    adapter_type = "vmxnet3"
  }

  disk {
    label = "disk0"
    size  = var.disksize == "" ? data.vsphere_virtual_machine.template-ubuntu22.disks.0.size : var.disksize
  }

  clone {
    template_uuid = data.vsphere_virtual_machine.template-ubuntu22.id
    customize {
      linux_options {
        host_name = var.hostname
        domain    = "asadc.local"
      }
      network_interface {
        ipv4_address = var.ip_addr
        ipv4_netmask = var.cidr
      }
      ipv4_gateway    = var.defaultGW
      dns_server_list = [var.dns_server1, var.dns_server2]
    }
  }
  extra_config = {
    "guestinfo.userdata"          = base64encode(templatefile("${path.module}/userdata.yml", local.templatevars))
    "guestinfo.userdata.encoding" = "base64"
  }
}