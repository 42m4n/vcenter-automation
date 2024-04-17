from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='./common/configs.env')


class Path:
    vm_modules_path = 'modules'


class TerraformConf:
    base_init_path = 'terraform/'
    template_path = './terraform/terraform.tfvars.j2'
    variables_path = './terraform/terraform.tfvars'
    binary_path = ".terraform/providers/registry.terraform.io/hashicorp/vsphere/2.1.1/linux_amd64/terraform-provider-vsphere"
    chmode = 0o755


class VCenterConf:
    user = os.getenv("VSPHERE_USER")
    password = os.getenv("VSPHERE_PASSWORD")
    vcenter_address = os.getenv("VSPHERE_VCENTER")
