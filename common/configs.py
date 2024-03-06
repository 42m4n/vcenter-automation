class Path:
    vm_modules_path = './modules'


class TerraformConf:
    base_init_path = './terraform1/'
    template_path = 'terraform/terraform.tfvars.j2'
    variables_path = 'terraform/terraform.tfvars'
    binary_path = ".terraform/providers/registry.terraform.io/hashicorp/vsphere/2.1.1/linux_amd64/terraform-provider-vsphere"
    chmode = 0o755
