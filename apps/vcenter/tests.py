from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse


class TestCreateVMView(TestCase):
    def setUp(self):
        # Mock the necessary functions
        self.mock_create_module = patch('apps.vcenter.views.create_terraform_module').start()
        self.mock_render_template = patch('apps.vcenter.views.render_template').start()
        self.mock_apply_terraform = patch('apps.vcenter.views.apply_terraform_module').start()

        self.mock_create_module.return_value = 'modules/test_modules/'
        self.mock_render_template.return_value = 'ok'
        self.manage_engine_request_content = '''{
    "request": {
        "ola_due_by_time": null,
        "resolution": {
            "resolution_attachments": [],
            "content": null
        },
        "onhold_time": null,
        "has_purchase_requests": false,
        "is_trashed": false,
        "id": "841",
        "assigned_time": {
            "display_value": "2024/04/08 10:23",
            "value": "1712559195750"
        },
        "udf_fields": {
            "udf_pick_5415": "Test",
            "udf_pick_5416": "New Cluster",
            "udf_pick_5417": "datastore1",
            "udf_pick_5418": "VM Network",
            "udf_sline_3927": "unit test",
            "udf_sline_1524": "4",
            "udf_long_5420": "2",
            "udf_sline_1525": "4",
            "udf_pick_5434": "centos7_64Guest",
            "udf_pick_5422": "vmxnet3",
            "udf_sline_5423": "8",
            "udf_sline_5424": "any",
            "udf_sline_4560": null,
            "udf_sline_4202": "any",
            "udf_sline_4203": "50300",
            "udf_pick_3016": "Grant",
            "udf_pick_3017": "Always"
        },

    "response_status": {
        "status_code": 2000,
        "status": "success"
    }}
}'''

    def tearDown(self):
        # Stop the patching
        patch.stopall()

    def test_successful_vm_creation(self):
        self.mock_create_module.return_value = 'modules/test_modules/'
        self.mock_render_template.return_value = 'ok'
        self.mock_apply_terraform.return_value = {'result': 'success'}

        data = {
            'content': self.manage_engine_request_content
        }

        response = self.client.post(reverse('create_machine'), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'terraform_result': {'result': 'success'}})

    def test_unsuccessful_vm_creation(self):
        self.mock_create_module.return_value = 'modules/test_modules/'
        self.mock_render_template.return_value = 'ok'
        self.mock_apply_terraform.return_value = {'error': ''}

        data = {
            'content': self.manage_engine_request_content
        }

        response = self.client.post(reverse('create_machine'), data=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'terraform_result': {'error': ''}})
