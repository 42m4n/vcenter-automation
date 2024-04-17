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


variable "datacenter" {
}

variable "cluster" {
}


#=========================#
# vSphere virtual machine #
#=========================#


variable "datastore" {
}

variable "network" {
}

variable "name" {
}


variable "cpu" {
}

variable "ram" {
}

variable "guest_os" {
}
variable "network_adapter_type" {
}


variable "disk_size" {
}


variable "disk_label" {
}

variable "num_cores_per_socket" {
}
