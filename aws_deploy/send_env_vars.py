#!/usr/bin/env python

import os
import sys
import yaml
from py_eb_deployment import *

HELPER_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

config_file_name = "{0}/config.yaml".format(HELPER_PROJECT_ROOT)

if __name__=="__main__":

    project_exports_path = os.getenv("PROJECT_EXPORTS_PATH")

    if not project_exports_path:
        print("ERROR: Set PROJECT_EXPORTS_PATH to locate project environment files")

    with open(config_file_name, "r") as config_fil:
        config_dict = yaml.safe_load(config_fil)

    if not config_dict:
        print("ERROR: Unable to load config file: {0}".format(config_file_name))
        exit(1)

    project_name = config_dict.get('project_name', None)
    if not project_name:
        print("ERROR: 'project_name' not found in config file")
        exit(1)

    secure_env_dir = os.path.join(project_exports_path, 'projects', project_name)
    if not os.path.isdir(secure_env_dir):
        print("ERROR: '{0}' does not exist or is not a directory".format(secure_env_dir))
        exit(1)

    aws_account_dict = config_dict.get('aws_account_dict', {})
    eb_env_dict = config_dict.get('eb_env_dict', {})

    sev = EbDeployment(project_name,
                       aws_account_dict=aws_account_dict,
                       eb_env_dict=eb_env_dict)

    if len(sys.argv) > 1 and sys.argv[1] == 'usage':
        sev.print_usage()
        exit(0)

    if len(sys.argv) < 3:
        sev.print_usage()
        exit(1)

    aws_account_key = sys.argv[1]
    eb_env_key = sys.argv[2]

    try:
        sev.send_env_vars(secure_env_dir,
                          aws_account_key,
                          eb_env_key)
    except EbDeploymentException as sevse:
        print(sevse.message)
        sev.print_usage()

