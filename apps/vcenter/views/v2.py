from loguru import logger
from rest_framework import response, views

from apps.vcenter.serializers.v2 import CreateVMSerializer, UpdateVMSerializer
from common.configs import TerraformConf, VCenterConf
from common.modules.manage_engine import ManageEngine
from common.modules.terraform_utils import (apply_terraform_module,
                                            create_terraform_module,
                                            get_module_path, keep_old_version,
                                            read_existing_tfvars,
                                            render_template)


class CreateVMView(views.APIView):
    def post(self, request):
        try:
            serializer = CreateVMSerializer(data=request.data)
            if serializer.is_valid():
                terraform_vars = serializer.validated_data
                terraform_vars.update(
                    {
                        "vsphere_user": VCenterConf.user,
                        "vsphere_vcenter": VCenterConf.vcenter_address,
                    }
                )
                ticket_id = terraform_vars["ticket_id"]
                vm_name = terraform_vars["name"]
                module_path = create_terraform_module(vm_name)
                log_file = f"{module_path}/{vm_name}_creation.log"
                logger.add(log_file)
                logger.info(f"Starting VM creation process for {vm_name}")
                render_template(
                    TerraformConf.template_path,
                    terraform_vars,
                    f"{module_path}/terraform.tfvars",
                )
                logger.info(f"Rendered terraform.tfvars for {vm_name}")
                tf_result = apply_terraform_module(module_path, ticket_id, vm_name)
                logger.info(f"Terraform apply result for {vm_name}: {tf_result}")
                if "error" in tf_result:
                    logger.error(f"Error in apply for {vm_name}: {tf_result['error']}")
                    return response.Response(
                        {"terraform_result": tf_result}, status=400
                    )

                return response.Response({"terraform_result": tf_result})
            else:
                logger.error(f"Serializer error: {serializer.errors}")
                return response.Response(serializer.errors, status=400)
        except Exception as e:
            logger.exception(f"Exception in CreateVMView for {vm_name}: {str(e)}")
            note = f"Creation of {vm_name} vm was failed 😟. Check logs."
            ManageEngine().add_note_to_ticket(ticket_id, note)
            return response.Response({"error": str(e)}, status=400)

    def put(self, request, vm_name=None):
        try:

            serializer = UpdateVMSerializer(data=request.data)
            if serializer.is_valid():
                module_path = get_module_path(vm_name)
                terraform_vars = read_existing_tfvars(f"{module_path}/terraform.tfvars")
                terraform_vars.update(serializer.validated_data)
                terraform_vars.update(
                    {
                        "vsphere_user": VCenterConf.user,
                        "vsphere_vcenter": VCenterConf.vcenter_address,
                    }
                )
                ticket_id = terraform_vars["ticket_id"]
                keep_old_version(module_path)
                logger.info(f"old version of {vm_name} copied")
                render_template(
                    TerraformConf.template_path,
                    terraform_vars,
                    f"{module_path}/terraform.tfvars",
                )
                tf_result = apply_terraform_module(
                    module_path=module_path,
                    ticket_id=ticket_id,
                    vm_name=vm_name,
                    created=False,
                )
                if "error" in tf_result:
                    print("error in apply in view")
                    print("terraform_result", tf_result)
                    return response.Response(
                        {"terraform_result": tf_result}, status=400
                    )

                return response.Response({"terraform_result": tf_result})

            return response.Response(serializer.errors, status=400)

        except Exception as e:
            note = f"Update {vm_name} request failed. Check logs."
            ManageEngine().add_note_to_ticket(ticket_id, note)
            return response.Response({"error": str(e)}, status=400)
