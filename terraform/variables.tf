#====================#
# vCenter connection #
#====================#

variable "vsphere_user" {
}

variable "vsphere_password" {
}

variable "vsphere_server" {
}

variable "vsphere_unverified_ssl" {
  default = false
}

variable "datacenter" {
}

variable "cluster" {
}

#=========================#
# vSphere virtual machine #
#=========================#
variable "dvswitch" {

}

variable "folder" {

}

variable "datastore" {
}

variable "network" {
  default = "VM Network"
}

variable "name" {
}

variable "cpu" {
}

variable "ram" {
}

variable "disksize" {
  default = ""
}

variable "template-name" {
  type = string
}

variable "vlan_id" {
  type = number
}

#=========================#
#           OS            #
#=========================#

variable "hostname" {
  type = string
}

variable "ip_addr" {
  type = string
}

variable "cidr" {
  type = number
}

variable "defaultGW" {
  type = string
}

variable "dns_server1" {
  type    = string
  default = "172.20.28.41"
}

variable "dns_server2" {
  type    = string
  default = "172.20.28.42"
}