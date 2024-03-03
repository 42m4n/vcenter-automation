import shutil
from datetime import date
from random import randint

from jinja2 import Template
from python_terraform import Terraform

from common.configs import Path, TerraformConf


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


def create_terraform_module(vm_name, module_path=Path.vm_modules_path):
    try:
        unique_name = generate_module_name(vm_name)
        module_path = f"{module_path}/{unique_name}"
        shutil.copytree(TerraformConf.base_init_path, module_path)
        return module_path
    except Exception as e:
        print('Error at render create terraform module:')
        print(e)
        raise e


def apply_terraform_module(module_path):
    try:
        tf = Terraform(working_dir=module_path)
        tf.apply(skip_plan=True)
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
