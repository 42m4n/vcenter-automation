terraform {
  required_providers {
    vsphere = {
      source  = "hashicorp/vsphere"
      version = "2.1.1"
    }
  }
}
provider "vsphere" {
  user           = var.vsphere_user
  password       = var.vsphere_password
  vsphere_server = var.vsphere_vcenter
  allow_unverified_ssl = var.vsphere_unverified_ssl
}
