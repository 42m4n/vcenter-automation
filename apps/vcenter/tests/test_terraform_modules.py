import os
import shutil

from django.test import TestCase

from common.modules.terraform_utils import render_template, check_directory_existence, format_terraform_result


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
    ...


class GenerateModuleNameTestCase(TestCase):
    ...


class InitializeTerraformTestCase(TestCase):
    ...


class GetModulePathTestCase(TestCase):
    ...


class KeepOldVersionTestCase(TestCase):
    ...
