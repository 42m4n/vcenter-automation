import os
import shutil
from datetime import date
from unittest.mock import patch, MagicMock

from django.test import TestCase

from common.configs import Path
from common.exceptions import VMDirectoryExistsException
from common.modules.terraform_utils import render_template, check_directory_existence, format_terraform_result, \
    generate_module_name, keep_old_version, get_module_path, apply_terraform_module


class RenderTemplateTestCase(TestCase):
    def setUp(self):
        self.test_directory = 'test_dir'
        os.makedirs(self.test_directory, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_directory)

    def test_render_template(self):
        template_path = 'terraform/terraform.tfvars'
        variables = {'key': 'value'}
        result_dir = 'test_dir'
        result_path = f'{result_dir}/result.tfvars'
        os.makedirs(result_dir, exist_ok=True)

        result = render_template(template_path, variables, result_path)
        self.assertEqual(result, 'ok')

    def test_render_template_exception(self):
        template_path = 'non_existent_template.tfvars'
        variables = {}
        result_path = f'{self.test_directory}/result.tfvars'

        with self.assertRaises(Exception):
            render_template(template_path, variables, result_path)


class CheckDirectoryExistenceTestCase(TestCase):
    def setUp(self):
        self.test_directory = 'test_dir'
        self.test_vm_name_1 = 'test_vm_name_1'
        self.test_vm_name_2 = 'test_vm_name_2'
        self.exist_vm_path = os.path.join(self.test_directory, self.test_vm_name_1)
        os.makedirs(self.exist_vm_path, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_directory)

    def test_directory_exists(self):
        self.assertTrue(check_directory_existence(self.test_vm_name_1, self.test_directory))

    def test_directory_not_exists(self):
        self.assertFalse(check_directory_existence(self.test_vm_name_2, self.test_directory))


class CreateTerraformModuleTestCase(TestCase):
    ...


class FormatTerraformResultTestCase(TestCase):
    def test_successful_execution(self):
        terraform_result = (0, "Plan: 1 to add, 2 to change, 3 to destroy", "")
        result_dict, success = format_terraform_result(terraform_result)
        self.assertTrue(success)
        self.assertEqual(result_dict['add'], 1)
        self.assertEqual(result_dict['change'], 2)
        self.assertEqual(result_dict['destroy'], 3)

    def test_failed_execution(self):
        terraform_result = (1, "", "Error: Something went wrong")
        result_dict, success = format_terraform_result(terraform_result)
        self.assertFalse(success)
        self.assertEqual(result_dict['error'], "Error: Something went wrong")

    def test_exception_handling(self):
        with self.assertRaises(Exception):
            terraform_result = (1, "")
            format_terraform_result(terraform_result)


class ApplyTerraformModuleTestCase(TestCase):
    @patch('common.modules.terraform_utils.Terraform')
    @patch('common.modules.manage_engine.ManageEngine.add_note_to_ticket')
    @patch('common.modules.terraform_utils.format_terraform_result')
    def test_apply_terraform_module_success(self, mock_format_terraform_result, mock_manage_engine_note,
                                            mock_terraform):
        mock_tf_instance = MagicMock()
        mock_tf_instance.apply.return_value = (0, 'mocked_terraform_result', 'error')
        mock_terraform.return_value = mock_tf_instance

        mock_manage_engine_note.return_value = ''
        mock_format_terraform_result.return_value = ({"add": 1, "change": 2, "destroy": 0}, True)

        result = apply_terraform_module('mock_module_path', 'mock_ticket_id', 'mock_vm_name', created=True)

        mock_tf_instance.apply.assert_called_once_with(skip_plan=True)
        mock_manage_engine_note.assert_called_once_with('mock_ticket_id', 'VM mock_vm_name created successfully.')
        self.assertEqual(result, {"add": 1, "change": 2, "destroy": 0})


class GenerateModuleNameTestCase(TestCase):

    def test_generate_module_name(self):
        vm_name = "test_vm"
        expected_prefix = str(date.today()).replace("-", "_")
        unique_name = generate_module_name(vm_name)

        self.assertTrue(unique_name.startswith(expected_prefix))
        self.assertTrue(vm_name in unique_name)


class InitializeTerraformTestCase(TestCase):
    ...


class GetModulePathTestCase(TestCase):
    def setUp(self):
        self.test_directory = 'test_dir'
        self.test_vm_name_1 = '2024_12_11_222_test_vm_name_1'
        self.exist_vm_path = os.path.join(self.test_directory, self.test_vm_name_1)

        os.makedirs(self.exist_vm_path, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_directory)

    def test_get_module_path_found(self):
        exist_vm_path = os.path.join(Path.vm_modules_path, self.test_vm_name_1)
        os.makedirs(exist_vm_path, exist_ok=True)
        path = get_module_path(self.test_vm_name_1)
        self.assertEqual(path, f'{Path.vm_modules_path}/{self.test_vm_name_1}')
        shutil.rmtree(self.test_vm_name_1)

    @patch('os.listdir')
    def test_get_module_path_not_found(self, mock_listdir):
        mock_listdir.return_value = [' other_dir']
        with self.assertRaises(VMDirectoryExistsException):
            get_module_path('vm_name')

    @patch('os.listdir')
    def test_get_module_path_exception(self, mock_listdir):
        mock_listdir.side_effect = Exception('Mocked exception')
        with self.assertRaises(Exception):
            get_module_path('vm_name')


class KeepOldVersionTestCase(TestCase):
    def setUp(self):
        self.test_directory = 'test_dir'

    @patch('os.makedirs')
    @patch('shutil.copy')
    def test_keep_old_version_success(self, mock_copy, mock_makedirs):
        keep_old_version(self.test_directory)
        mock_makedirs.assert_called_once_with(f'{self.test_directory}/old', exist_ok=True)
        mock_copy.assert_called_once()

    @patch('os.makedirs', side_effect=Exception('Mocked exception'))
    def test_keep_old_version_exception(self, mock_makedirs):
        with self.assertRaises(Exception):
            keep_old_version(self.test_directory)
