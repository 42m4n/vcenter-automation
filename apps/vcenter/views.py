from rest_framework import views, response

from apps.vcenter.serializers import CreateVMSerializer
from common.configs import TerraformConf
from common.utilities import render_template, create_terraform_module, apply_terraform_module


class CreateVMView(views.APIView):
    def post(self, request):
        serializer = CreateVMSerializer(data=request.data)
        if serializer.is_valid():
            terraform_vars = serializer.validated_data
            module_path = create_terraform_module(terraform_vars['vm_name'])
            render_template(TerraformConf.template_path, terraform_vars,
                            f'{module_path}/terraform.tfvars')
            tf_result = apply_terraform_module(module_path)
            return response.Response({'terraform_result': tf_result})
        return response.Response(serializer.errors, status=400)
