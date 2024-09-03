import os


class Path:
    vm_modules_path = "modules"


class TerraformConf:
    base_init_path = "terraform/"
    template_path = "./terraform/terraform.tfvars.j2"
    variables_path = "./terraform/terraform.tfvars"
    binary_path = ".terraform/providers/"
    chmod = 0o755


class VCenterConf:
    user = os.getenv("VSPHERE_USER")
    vcenter_address = os.getenv("VSPHERE_VCENTER")


class ManageEngineConf:
    manage_engine_address = os.getenv("MANAGE_ENGINE_ADDRESS")
    manage_engine_token = os.getenv("MANAGE_ENGINE_TOKEN")
    manage_engine_done_status = os.getenv("MANAGE_ENGINE_DONE_STATUS", "4")
    udf_fields_mapping = {
        "udf_pick_5415": "datacenter",
        "udf_pick_5416": "cluster",
        "udf_pick_5417": "datastore",
        "udf_pick_5418": "network",
        "udf_sline_3927": "name",
        "udf_sline_1524": "cpu",
        "udf_long_5420": "num_cores_per_socket",
        "udf_sline_1525": "ram",
        "udf_pick_5434": "guest_os",
        "udf_pick_5422": "network_adapter_type",
        "udf_sline_5423": "disk_size",
        "udf_sline_5424": "disk_label",
    }
