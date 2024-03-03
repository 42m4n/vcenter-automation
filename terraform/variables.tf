#====================#
# vCenter connection #
#====================#

variable "vsphere_user" {
}

variable "vsphere_password" {
}

variable "vsphere_vcenter" {
}

variable "vsphere_unverified_ssl" {
}


variable "vsphere_datacenter" {
}

variable "vsphere_cluster" {
}


#=========================#
# vSphere virtual machine #
#=========================#


variable "vm_datastore" {
}

variable "vm_network" {
}

variable "vm_name" {
}


variable "vm_cpu" {
}

variable "vm_ram" {
}

variable "vm_guest" {
}
variable "vm_network_adapter_type" {
}


variable "vm_disk_size" {
}


variable "vm_disk_label" {
}