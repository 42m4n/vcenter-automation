import shutil
from datetime import date
from random import randint
import re
import os
from jinja2 import Template
from python_terraform import Terraform

from common.configs import Path, TerraformConf
from common.exceptions import VMDirectoryExistsException


def render_template(template_path, variables, result_path):
    try:
        with open(template_path) as file:
            template = Template(file.read())
            render_result = template.render(variables)
            with open(result_path, 'a+') as var_file:
                var_file.write(render_result)
            # ToDo: return proper result
            return 'hi'
    except Exception as e:
        print('Error at render template:')
        print(e)
        raise e


def check_directory_existence(vm_name, directory_path=Path.vm_modules_path):
    for root, dirs, files in os.walk(directory_path):
        for dir in dirs:
            if vm_name in dir:
                return True
    return False


def create_terraform_module(vm_name, module_path=Path.vm_modules_path):
    try:
        created = check_directory_existence(vm_name)
        if not created:
            unique_name = generate_module_name(vm_name)
            module_path = f"{module_path}/{unique_name}"
            shutil.copytree(TerraformConf.base_init_path, module_path)
            return module_path
        else:
            raise VMDirectoryExistsException('Directory already exists.')

    except Exception as e:
        print('Error at render create terraform module:')
        print(e)
        raise e


def format_terraform_result(terraform_result):
    ret_code, out, err = terraform_result
    result_dict = {}
    if ret_code == 0:
        output = re.findall(r'Plan: (\d+) to add, (\d+) to change, (\d+) to destroy', out)
        result_dict['add'], result_dict['change'], result_dict['destroy'] = map(int, output[0])
    else:
        result_dict['error'] = str(err)
    return result_dict


def apply_terraform_module(module_path):
    try:
        tf = Terraform(working_dir=module_path)
        terraform_result = tf.apply(skip_plan=True)
        formatted_result = format_terraform_result(terraform_result)
        return formatted_result
    except Exception as e:
        print('Error at apply terraform :')
        print(e)
        raise e


def generate_module_name(vm_name):
    today = str(date.today()).replace("-", "_")
    unique_name = f"{today}_{vm_name}_{randint(1, 100000)}"

    return unique_name


def initialize_terraform(working_dir):
    try:
        tf = Terraform(working_dir=working_dir)
        tf.init()
    except Exception:
        pass


def get_module_path(vm_name, module_path=Path.vm_modules_path):
    for root, dirs, files in os.walk(module_path):
        if vm_name in dirs:
            return os.path.join(root, vm_name)
    return None
