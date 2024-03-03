from rest_framework import views, response

from apps.vcenter.serializers import CreateVMSerializer, UpdateVMSerializer
from common.configs import TerraformConf
from common.utilities import render_template, create_terraform_module, apply_terraform_module, get_module_path


class CreateVMView(views.APIView):
    def post(self, request):
        try:
            serializer = CreateVMSerializer(data=request.data)
            if serializer.is_valid():
                terraform_vars = serializer.validated_data
                module_path = create_terraform_module(terraform_vars['vm_name'])
                render_template(TerraformConf.template_path, terraform_vars,
                                f'{module_path}/terraform.tfvars')
                tf_result = apply_terraform_module(module_path)
                # Todo: handle tf_result status code for errors in apply
                return response.Response({'terraform_result': tf_result})

            return response.Response(serializer.errors, status=400)

        except Exception as e:

            return response.Response({'error': str(e)}, status=400)

    def put(self, request, vm_name=None):

        serializer = UpdateVMSerializer(data=request.data)
        if serializer.is_valid():
            try:
                terraform_vars = serializer.validated_data
                terraform_vars['vm_name'] = vm_name

                module_path = get_module_path(vm_name)
                render_template(TerraformConf.template_path, terraform_vars,
                                f'{module_path}/terraform.tfvars')
                tf_result = apply_terraform_module(module_path)
                # Todo: handle tf_result status code for errors in apply
                return response.Response({'terraform_result': tf_result})
            except Exception as e:

                return response.Response({'error': str(e)}, status=400)
        return response.Response(serializer.errors, status=400)
