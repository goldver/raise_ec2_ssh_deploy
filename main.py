#!/usr/bin/python
from raise_instance import *
from deploy import *

# usage
# python3 main.py test prod 0 ami-d2xxxxab m4.large start

terraform_run(service_name, action)
deploy(service_name, env, scrum_num)
time.sleep(15)
check_alive(service_name, env)