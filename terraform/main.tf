
#===============================================================================
# vSphere Data
#===============================================================================

data "vsphere_datacenter" "dc" {
  name = var.vsphere_datacenter
}

data "vsphere_compute_cluster" "cluster" {
  name          = var.vsphere_cluster
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_datastore" "datastore" {
  name          = var.vm_datastore
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_network" "network" {
  name          = var.vm_network
  datacenter_id = data.vsphere_datacenter.dc.id
}

#===============================================================================
# vSphere Resources
#===============================================================================

resource "vsphere_virtual_machine" "standalone" {
  name             = var.vm_name
  resource_pool_id = data.vsphere_compute_cluster.cluster.resource_pool_id
  datastore_id     = data.vsphere_datastore.datastore.id

  wait_for_guest_net_timeout = 0
  wait_for_guest_ip_timeout  = 0

  num_cpus = var.vm_cpu
  memory   = var.vm_ram
  guest_id = var.vm_guest

  network_interface {
    network_id   = data.vsphere_network.network.id
    adapter_type   = var.vm_network_adapter_type
  }

  disk {
   size             = var.vm_disk_size
   label            =var.vm_disk_label
  }

}