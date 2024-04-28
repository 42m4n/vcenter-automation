import json

from rest_framework import views, response
from loguru import logger
from apps.vcenter.serializers import CreateVMSerializer, UpdateVMSerializer, ManageEngineSerializer
from common.configs import TerraformConf, VCenterConf
from common.modules.manage_engine import ManageEngine
from common.modules.terraform_utils import create_terraform_module, render_template, apply_terraform_module, \
    get_module_path, keep_old_version


class CreateVMView(views.APIView):
    def post(self, request):
        try:
            udf_serializer = ManageEngineSerializer(data=request.data)
            udf_serializer.is_valid(raise_exception=True)
            udf_data = json.loads(udf_serializer.validated_data.get('content'))
            ticket_request = udf_data.get('request')
            ticket_id = ticket_request.get('id')
            udf_fields = ticket_request.get('udf_fields')

            mapped_data = {}
            udf_fields_map = ManageEngine().udf_fields_mapping

            for key, value in udf_fields.items():
                if key in udf_fields_map:
                    mapped_data[udf_fields_map[key]] = value

            serializer = CreateVMSerializer(data=mapped_data)
            if serializer.is_valid():
                terraform_vars = serializer.validated_data
                terraform_vars.update({
                    'vsphere_user': VCenterConf.user,
                    'vsphere_password': VCenterConf.password,
                    'vsphere_vcenter': VCenterConf.vcenter_address
                })
                vm_name = terraform_vars['name']
                module_path = create_terraform_module(vm_name)
                render_template(TerraformConf.template_path, terraform_vars,
                                f'{module_path}/terraform.tfvars')
                print('after render')

                tf_result = apply_terraform_module(module_path, ticket_id, vm_name)
                print('after apply in view')
                if 'error' in tf_result:
                    print('error in apply in view')
                    print('terraform_result', tf_result)
                    return response.Response({'terraform_result': tf_result}, status=400)

                return response.Response({'terraform_result': tf_result})
            else:
                print('error in serializer in view')
                note = f'Create machin request failed. Check logs.'
                ManageEngine().add_note_to_ticket(ticket_id, note)
                return response.Response(serializer.errors, status=400)
        except Exception as e:
            print('>>>>>>>>>>>>>Exception in view:')
            print(e)
            note = f'Create {vm_name} failed. Check logs.'
            ManageEngine().add_note_to_ticket(ticket_id, note)
            return response.Response({'error': str(e)}, status=400)

    def put(self, request, vm_name=None):
        try:

            udf_serializer = ManageEngineSerializer(data=request.data)
            udf_serializer.is_valid(raise_exception=True)
            udf_data = json.loads(udf_serializer.validated_data.get('content'))
            ticket_request = udf_data.get('request')
            ticket_id = ticket_request.get('id')
            udf_fields = ticket_request.get('udf_fields')

            mapped_data = {}
            udf_fields_map = ManageEngine().udf_fields_mapping
            for key, value in udf_fields.items():
                if key in udf_fields_map:
                    mapped_data[udf_fields_map[key]] = value

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
                logger.info(f'old version of {vm_name} copied')
                render_template(TerraformConf.template_path, terraform_vars,
                                f'{module_path}/terraform.tfvars')
                tf_result = apply_terraform_module(module_path, ticket_id=ticket_id, vm_name=vm_name, created=False)
                if 'error' in tf_result:
                    print('error in apply in view')
                    print('terraform_result', tf_result)
                    return response.Response({'terraform_result': tf_result}, status=400)

                return response.Response({'terraform_result': tf_result})
            note = f'Update {vm_name} request failed. Check logs.'
            ManageEngine().add_note_to_ticket(ticket_id, note)
            return response.Response(serializer.errors, status=400)

        except Exception as e:
            note = f'Update {vm_name} failed. Check logs.'
            ManageEngine().add_note_to_ticket(ticket_id, note)
            return response.Response({'error': str(e)}, status=400)
