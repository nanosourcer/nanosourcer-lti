#!/usr/bin/env python

import os, sys
import yaml
import shlex, subprocess
from subprocess import PIPE

app_name = "nanosourcer"
project = "django-{0}".format(app_name)
env_dir = "~/project_exports/projects/{0}".format(project)

site_dict = {'beta': '{0}-beta'.format(app_name),
             'prod': '{0}'.format(app_name)}

aws_account_alias_dict = {'main': 'ls-lta'}

if len(sys.argv) < 2 or sys.argv[1] not in site_dict:
    print("\nUsage: {0} <site-name> <aws-account-alias>\n".format(sys.argv[0]))
    print("Provide a valid site name:")
    for k,v  in site_dict.items():
        print("\t{0}".format(k))
    print("Provide a valid AWS account alias:")
    for k,v  in aws_account_alias_dict.items():
        print("\t{0}".format(k))
    print("")
    exit(1)

if len(sys.argv) < 3 or sys.argv[2] not in aws_account_alias_dict:
    print("Provide a valid AWS account alias:")
    for k,v  in aws_account_alias_dict.items():
        print("\t{0}".format(k))
    print("")
    exit(1)

site = sys.argv[1]
aws_account_alias = sys.argv[2]

aws_account_name = aws_account_alias_dict[aws_account_alias]

env_fil = os.path.expanduser("{0}/env.{1}.{2}.{3}.cfg".format(env_dir, project, aws_account_name, site))

with open(env_fil, "r") as fil:

    config_dict = yaml.safe_load(fil)

    if not config_dict:

        print("ERROR: Unable to load environment vars file: {0}".format(env_fil))

    else:

        site_environment = site_dict[site]

        env_str = " ".join('{0}=\'{1}\''.format(k, v) for k,v in config_dict.items())

        eb_cmd = "eb setenv {1} -e {0} --quiet --profile {2}".format(site_environment, env_str, aws_account_name)

        print("eb_cmd: {0}".format(eb_cmd))

        args = shlex.split(eb_cmd)
        p = subprocess.Popen(args, stdin=PIPE, stdout=PIPE)
        (stdout, stderr) = p.communicate()
        outlist = stdout.split('\n')
        for o in outlist:
            print(o)
            sys.stdout.flush()

        print("Submitted environment vars update to {0}: {1}\n".format(project, site))

