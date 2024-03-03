from rest_framework import views, response

from apps.vcenter.serializers import CreateVMSerializer
from common.configs import TerraformConf
from common.utilities import render_template, create_terraform_module, apply_terraform_module


class CreateVMView(views.APIView):
    def post(self, request):
        serializer = CreateVMSerializer(data=request.data)
        if serializer.is_valid():
            terraform_vars = serializer.validated_data
            print('^^^^^')
            print(terraform_vars['vm_name'])
            module_path = create_terraform_module(terraform_vars['vm_name'])
            print('MP:')
            print(module_path)
            rendered_template = render_template(TerraformConf.template_path, terraform_vars,
                                                f'{module_path}/terraform.tfvars')
            print('render done')
            apply_terraform_module(module_path)
            return response.Response({'terraform_vars': rendered_template})
        return response.Response(serializer.errors, status=400)
