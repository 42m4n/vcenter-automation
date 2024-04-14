import json

from rest_framework import views, response

from apps.vcenter.serializers import CreateVMSerializer, UpdateVMSerializer, ManageEngineSerializer
from common.configs import TerraformConf, VCenterConf, udf_fields_mapping
from common.utilities import render_template, create_terraform_module, apply_terraform_module, get_module_path, \
    keep_old_version


class CreateVMView(views.APIView):
    def post(self, request):
        try:

            udf_serializer = ManageEngineSerializer(data=request.data)
            udf_serializer.is_valid(raise_exception=True)
            udf_data = json.loads(udf_serializer.validated_data['content'])
            udf_fields = udf_data['request']['udf_fields']
            mapped_data = {}
            for key, value in udf_fields.items():
                if key in udf_fields_mapping:
                    mapped_data[udf_fields_mapping[key]] = value
            serializer = CreateVMSerializer(data=mapped_data)
            if serializer.is_valid():
                terraform_vars = serializer.validated_data
                terraform_vars.update({
                    'vsphere_user': VCenterConf.user,
                    'vsphere_password': VCenterConf.password,
                    'vsphere_vcenter': VCenterConf.vcenter_address
                })
                module_path = create_terraform_module(terraform_vars['name'])
                render_template(TerraformConf.template_path, terraform_vars,
                                f'{module_path}/terraform.tfvars')

                tf_result = apply_terraform_module(module_path)
                return response.Response({'terraform_result': tf_result})
            else:
                return response.Response(serializer.errors, status=400)
        except Exception as e:

            return response.Response({'error': str(e)}, status=400)

    def put(self, request, vm_name=None):
        try:

            udf_serializer = ManageEngineSerializer(data=request.data)
            udf_serializer.is_valid(raise_exception=True)
            udf_data = json.loads(udf_serializer.validated_data['content'])
            udf_fields = udf_data['request']['udf_fields']
            mapped_data = {}
            for key, value in udf_fields.items():
                if key in udf_fields_mapping:
                    mapped_data[udf_fields_mapping[key]] = value

            serializer = UpdateVMSerializer(data=mapped_data)
            if serializer.is_valid():
                terraform_vars = serializer.validated_data
                terraform_vars.update({
                    'name': vm_name,
                    'vsphere_user': VCenterConf.user,
                    'vsphere_password': VCenterConf.password,
                    'vsphere_vcenter': VCenterConf.vcenter_address
                })
                module_path = get_module_path(vm_name)
                keep_old_version(module_path)
                render_template(TerraformConf.template_path, terraform_vars,
                                f'{module_path}/terraform.tfvars')
                tf_result = apply_terraform_module(module_path)
                # Todo: handle tf_result status code for errors in apply
                return response.Response({'terraform_result': tf_result})

            return response.Response(serializer.errors, status=400)

        except Exception as e:

            return response.Response({'error': str(e)}, status=400)
