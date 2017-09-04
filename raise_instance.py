#!/usr/bin/python
import os
import boto3
import sys

ec2 = boto3.client("ec2")

service_name = str(sys.argv[1])
env = str(sys.argv[2])
scrum_num = str(sys.argv[3])
ami_id = str(sys.argv[4])  # ami-d2xxxxab
inst_type = str(sys.argv[5])  # m4.large
action = str(sys.argv[6])


# get subnet
def get_subnet(scrum_num):
    ec2 = boto3.client('ec2')
    subnet = ec2.describe_subnets(Filters=[
        {
            'Name': 'tag:Name',
            'Values': ["scrum" + scrum_num]
        }
    ])
    return subnet['Subnets'][0]['SubnetId']


# find security group to set up terraform files
def find_sg(service_name):
    if env == 'prod':
        resp = ec2.describe_security_groups(Filters=[{'Name': 'group-name', 'Values': [service_name + '-prod']}])
    else:
        resp = ec2.describe_security_groups(Filters=[{'Name': 'group-name', 'Values': [service_name]}])

    for sg in resp['SecurityGroups']:
        parse_sg = {'name': sg['GroupName'], 'groupid': sg['GroupId']}
        print(parse_sg)

        service_sg = parse_sg['groupid']
        print(service_sg)
        return service_sg


if env == 'prod':
    subnets = "subnet-50xxxa19,subnet-0fxxxa68,subnet-41xxxx19"
else:
    subnets = get_subnet(scrum_num)

access_key = os.environ['ACCESS_KEY']
secret_key = os.environ['SECRET_KEY']
service = service_name
vpc_id = 'vpc-adxxxxc9'
sec_group = find_sg(service_name)
instance_type = inst_type
subnets = subnets
hostname = service_name + "-test"


# terraform cmd
def terraform_action(action):
    if action in ['start']:
        return 'apply'
    else:
        return 'destroy'


# Terraform actions
def terraform_run(service_name, action):
    os.system("terraform init")
    action = terraform_action(action)

    force = ''
    if action == "destroy":
        force = "-force"

    terraform_init = "terraform init \
     -force-copy"

    os.system(terraform_init + " && terraform " + action + " \
        -backup=- \
        -var 'access_key=" + access_key + "' \
        -var 'secret_key=" + secret_key + "' \
        -var 'vpc_id=" + vpc_id + "' \
        -var 'service=" + service + "' \
        -var 'sec_group=" + sec_group + "' \
        -var 'instance_type=" + instance_type + "' \
        -var 'subnets=" + subnets + "' \
        -var 'ami=" + ami_id + "' \
        -var 'hostname=" + hostname + "' \
        " + force + " ")

    if action == 'destroy':
        exit(0)
