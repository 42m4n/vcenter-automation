import json

from rest_framework import views, response

from apps.vcenter.serializers import CreateVMSerializer, UpdateVMSerializer, ManageEngineSerializer
from common.configs import TerraformConf, VCenterConf
from common.utilities import render_template, create_terraform_module, apply_terraform_module, get_module_path, \
    keep_old_version

udf_fields_mapping = {
    "udf_pick_5415": "datacenter",
    "udf_pick_5416": "cluster",
    "udf_pick_5417": "datastore",
    "udf_pick_5418": "network",
    "udf_sline_5419": "name",
    "udf_sline_1524": "cpu",
    "udf_long_5420": "num_cores_per_socket",
    "udf_sline_1525": "ram",
    "udf_sline_5425": "guest_os",
    "udf_pick_5422": "network_adapter_type",
    "udf_sline_5423": "disk_size",
    "udf_sline_5424": "disk_label",
}


class CreateVMView(views.APIView):
    def post(self, request):
        udf_serializer = ManageEngineSerializer(data=request.date)
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

    # class CreateVMView(views.APIView):
    #     def post(self, request):
    #         try:
    #             serializer = PaasSerializer(data=request.data)
    #             if serializer.is_valid(raise_exception=True):
    #                 if serializer.is_valid():
    #                     serializer_validated_data = json.loads(serializer.validated_data['content'])
    #                     print('****This is serializer data')
    #                     print(serializer_validated_data)
    #
    #             serializer = CreateVMSerializer(data=request.data)
    #             if serializer.is_valid():
    #                 serializer_validated_data = json.loads(serializer.validated_data['content'])
    #
    #                 terraform_vars = serializer.validated_data
    #                 terraform_vars.update({
    #                     'vsphere_user': VCenterConf.user,
    #                     'vsphere_password': VCenterConf.password,
    #                     'vsphere_vcenter': VCenterConf.vcenter_address
    #                 })
    #                 module_path = create_terraform_module(terraform_vars['name'])
    #                 render_template(TerraformConf.template_path, terraform_vars,
    #                                 f'{module_path}/terraform.tfvars')
    #
    #                 tf_result = apply_terraform_module(module_path)
    #                 # Todo: handle tf_result status code for errors in apply
    #                 return response.Response({'terraform_result': tf_result})
    #
    #             return response.Response(serializer.errors, status=400)
    #
    #         except Exception as e:
    #
    #             return response.Response({'error': str(e)}, status=400)

    def put(self, request, vm_name=None):

        serializer = UpdateVMSerializer(data=request.data)
        if serializer.is_valid():
            try:
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
            except Exception as e:

                return response.Response({'error': str(e)}, status=400)
        return response.Response(serializer.errors, status=400)
