#!/usr/bin/python
import os
import time
import subprocess

user = 'deploy'


# deploy role
def deploy(service_name, env, scrum_num):
    a = time.time()
    while True:
        cmd = "ssh -o 'StrictHostKeyChecking no' " + user + "@" + service_name + "-test.vvv.io" " \"df -h" "\""

        if env == "prod":
            run_deploy = "ssh -o 'StrictHostKeyChecking no' " + user + "@" \
                         + service_name + "-test.vvv.io" " \"sudo chef-client -o role[" + service_name + "-" + env + "] -l debug" "\""
        else:
            run_deploy = "ssh -o 'StrictHostKeyChecking no' " + user + "@" \
                         + service_name + "-test.vvv.io" " \"sudo chef-client -o role[" + service_name + "-" + env + scrum_num + "] -l debug" "\""
        try:
            print("\n")
            print("Service: %s-test, env: %s" % (service_name, env))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            subprocess.check_output(cmd, shell=True)
            print('\033[92mInstance %s-test is ready\033[0m' % service_name)
            print(run_deploy)
            os.system(run_deploy)
            break
        except:
            print('\033[93mWaiting for Instance: %s-test\033[0m' % service_name)
            if (time.time() - a) > 1800:
                print(':skull: Failed to connect to Instance %s-test, %s is not responding' % (service_name))
                exit(1)
        time.sleep(30)


# check alive after deploy
def check_alive(service_name, env):
    print("\n")
    print("Service: %s-test, env: %s" % (service_name, env))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    os.system("curl " + service_name + "-test.vvv.io/alive | jq")
