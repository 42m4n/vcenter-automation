import os
import re
import shutil
from datetime import date
from random import randint
from loguru import logger
from jinja2 import Template
from python_terraform import Terraform

from common.configs import Path, TerraformConf
from common.exceptions import VMDirectoryExistsException
from common.modules.manage_engine import ManageEngine


def render_template(template_path, variables, result_path):
    try:
        with open(template_path) as file:
            template = Template(file.read())
            render_result = template.render(variables)
            with open(result_path, 'w+') as var_file:
                logger.info(f'Render template: {result_path}')
                var_file.write(render_result)
            # ToDo: return proper result
            return 'ok'
    except Exception as e:
        print('Error at render template:')
        print(e)
        logger.error(f'Error at render template: {e}')
        raise e


def check_directory_existence(vm_name, directory_path=Path.vm_modules_path):
    for root, dirs, files in os.walk(directory_path):
        for dir in dirs:
            if vm_name in dir:
                return True
    return False


def create_terraform_module(vm_name, module_path=Path.vm_modules_path):
    try:
        logger.info(f'creating terraform module for {vm_name}')
        created = check_directory_existence(vm_name)
        if not created:
            unique_name = generate_module_name(vm_name)
            module_path = f"{module_path}/{unique_name}"
            shutil.copytree(src=TerraformConf.base_init_path,
                            dst=module_path,
                            ignore=shutil.ignore_patterns('.terraform', '.terraform.lock.hcl')
                            )
            print(os.system("pwd"))
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            os.symlink(src='../../terraform/.terraform', dst=module_path+'/.terraform', target_is_directory=True)
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            os.symlink(src='../../terraform/.terraform.lock.hcl', dst=module_path+'/.terraform.lock.hcl', target_is_directory=True)
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            logger.info(f'Base init path copied to {module_path}')
            target_file_path = f'{module_path}/{TerraformConf.binary_path}'
            os.chmod(target_file_path, TerraformConf.chmod)
            logger.info(f'{target_file_path} chmod changed')
            return module_path
        else:
            raise VMDirectoryExistsException('Directory already exists.')

    except Exception as e:
        print('Error at render create terraform module:')
        print(e)
        logger.error(f'Error at render create terraform module: {e}')
        raise e


def format_terraform_result(terraform_result):
    try:
        ret_code, out, err = terraform_result
        result_dict = {}
        success = True
        if ret_code == 0:
            output = re.findall(r'Plan: (\d+) to add, (\d+) to change, (\d+) to destroy', out)
            if output:
                result_dict['add'], result_dict['change'], result_dict['destroy'] = map(int, output[0])

        else:
            result_dict['error'] = str(err)
            success = False

        return result_dict, success
    except Exception as e:
        print('Error at format terraform result:')
        print(e)
        logger.error(f'Error at format terraform result {e}')

        raise e


def apply_terraform_module(module_path, ticket_id, vm_name, created=True):
    try:
        tf = Terraform(working_dir=module_path)
        terraform_result = tf.apply(skip_plan=True)
        logger.info(f'Terraform applied for  {module_path}')
        formatted_result, success = format_terraform_result(terraform_result)
        logger.info(f'Apply terraform for {vm_name} result: {success} , {terraform_result}')
        if success:
            note = f'VM {vm_name} {"created" if created else "updated"} successfully.'
        else:
            note = f'{"Create" if created else "Update"} VM {vm_name} failed.'

        ManageEngine().add_note_to_ticket(ticket_id, note)

        return formatted_result
    except Exception as e:
        print('Error at apply terraform :')
        print(e)
        note = f'Create VM {vm_name} failed.'
        ManageEngine().add_note_to_ticket(ticket_id, note)
        logger.error(f'apply terraform for {vm_name} failed cause: {e}')
        raise e


def generate_module_name(vm_name):
    today = str(date.today()).replace("-", "_")
    unique_name = f"{today}_{randint(1, 100000)}_{vm_name}"

    return unique_name


def initialize_terraform(working_dir):
    try:
        tf = Terraform(working_dir=working_dir)
        tf.init()
        logger.info(f'Terraform init in {working_dir}')
    except Exception as e:
        logger.error(f'Terraform inti failed cause: {e}')
        raise e


def get_module_path(vm_name):
    try:
        directories = [d for d in os.listdir(Path.vm_modules_path) if
                       os.path.isdir(os.path.join(Path.vm_modules_path, d))]
        for folder in directories:
            f_name = folder.split('_')
            f_name = '_'.join(f_name[4:])
            if f_name == vm_name:
                return f'{Path.vm_modules_path}/{folder}'
        logger.warning('No such file or directory for vm_name')
        raise VMDirectoryExistsException('No such file or directory')

    except Exception as e:
        print('Exception at get_module_path')
        print(e)
        logger.error(f'Get terraform module path failed cause: {e}')
        raise e


def keep_old_version(module_path):
    try:
        today = str(date.today()).replace("-", "_")
        rand_int = randint(1, 100000)
        os.makedirs(f'{module_path}/old', exist_ok=True)
        shutil.copy(f'{module_path}/main.tf', f'{module_path}/old/{today}_main_{rand_int}.tf')
    except Exception as e:
        print('Exception at keep_old_version')
        print(e)
        logger.error(f'Exception at keep_old_version : {e} ')
        raise e

def read_existing_tfvars(file_path):
    if not os.path.exists(file_path):
        return {}
    existing_vars = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"')
                existing_vars[key] = value
    return existing_vars