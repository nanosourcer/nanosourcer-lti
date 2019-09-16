import os, sys
import yaml
import shlex, subprocess
from subprocess import PIPE

class EbDeploymentException(Exception):

    def __init__(self, message):
        self.message = message

class EbDeployment(object):

    def __init__(self, 
                 project_name,
                 aws_account_dict=None,
                 eb_env_dict=None):

        self.project_name = project_name

        self.aws_account_dict = {} if not aws_account_dict else aws_account_dict
        self.eb_env_dict = {} if not eb_env_dict else eb_env_dict
     
    def send_env_vars(self,
                      secure_env_dir,
                      aws_account_key,
                      eb_env_key):

        aws_account_key = aws_account_key
        eb_env_key = eb_env_key

        if aws_account_key not in self.aws_account_dict:
            msg = "\nAWS account key not supported: {0}".format(aws_account_key)
            raise EbDeploymentException(msg)

        if eb_env_key not in self.eb_env_dict:
            msg = "\nEB environment key not supported: {0}".format(eb_env_key)
            raise EbDeploymentException(msg)

        aws_account = self.aws_account_dict[aws_account_key]
        eb_environment = self.eb_env_dict[eb_env_key]

        env_fil = os.path.expanduser("{0}/env.{1}.{2}.{3}.cfg".format(secure_env_dir, 
                                                                      self.project_name,
                                                                      aws_account,
                                                                      eb_env_key))

        with open(env_fil, "r") as fil:

            env_config_dict = yaml.safe_load(fil)

            if not env_config_dict:

                print("ERROR: Unable to load environment vars file: {0}".format(env_fil))

            else:

                env_str = " ".join('{0}="{1}"'.format(k, v) for k, v in env_config_dict.items())

                eb_cmd = "eb setenv {1} -e {0} --quiet --profile {2}".format(eb_environment, env_str, aws_account)

                args = shlex.split(eb_cmd)
                p = subprocess.Popen(args, stdin=PIPE, stdout=PIPE)
                (stdout, stderr) = p.communicate()
                outlist = stdout.split('\n')
                for o in outlist:
                    print(o)

                print("\nEnvironment variables have been sent to EB instance: {0}: {1}".format(aws_account,
                                                                                               eb_environment))
                print("EB instance will restart to update environment.\n")
                print("Run the following to monitor status/success/failure:\n\neb status {0} --profile {1}\n".format(eb_environment, 
                                                                                                                     aws_account))

    def deploy(self,
               aws_account_key,
               eb_env_key):

        aws_account_key = aws_account_key
        eb_env_key = eb_env_key

        if aws_account_key not in self.aws_account_dict:
            msg = "\nAWS account key not supported: {0}".format(aws_account_key)
            raise EbDeploymentException(msg)

        if eb_env_key not in self.eb_env_dict:
            msg = "\nEB environment key not supported: {0}".format(eb_env_key)
            raise EbDeploymentException(msg)

        aws_account = self.aws_account_dict[aws_account_key]
        eb_environment = self.eb_env_dict[eb_env_key]

        eb_cmd = "eb deploy {0} --profile {1}".format(eb_environment, aws_account)
 
        print(eb_cmd)

        # TODO - remove following when ready to send to actual EB instance
        print("Error: remove 'return' to really-truly process")
        return

        args = shlex.split(eb_cmd)
        p = subprocess.Popen(args, stdin=PIPE, stdout=PIPE)
        (stdout, stderr) = p.communicate()
        outlist = stdout.split('\n')
        for o in outlist:
            print(o)

        print("\nDeployment to EB instance: {0}: {1}".format(aws_account,
                                                             eb_environment))
        print("EB instance will restart to update environment.\n")
        print("Run the following to monitor status/success/failure:\n\neb status {0} --profile {1}\n".format(eb_environment, 
                                                                                                             aws_account))

    def construct_available_aws_account_info(self):
        msg = "Valid account keys for target AWS account:\n"
        msg = "{0}\t{1:20} {2}\n\t{3:20} {3}\n".format(msg, 'aws-account-key', 'account', '-' * 20, '-' * 20)
        for k, v in self.aws_account_dict.items():
            msg = "{0}{1}\n".format(msg, "\t{0:20} {1}".format(k, v))
        return msg

    def construct_available_eb_env_info(self):
        msg = "Valid environment keys for target EB environment:\n"
        msg = "{0}\t{1:20} {2}\n\t{3:20} {3}\n".format(msg, 'eb-environment-key', 'environment', '-' * 20, '-' * 20)
        for k, v in self.eb_env_dict.items():
            msg = "{0}{1}\n".format(msg, "\t{0:20} {1}".format(k, v))
        return msg

    def print_usage(self):
        print("\nUsage: {0} <aws-account-key> <eb-environment-key>\n".format(sys.argv[0]))
        print(self.construct_available_aws_account_info())
        print(self.construct_available_eb_env_info())

