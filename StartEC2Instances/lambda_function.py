import boto3
import os

# replace with your AWS region
region = 'us-west-1'
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    instances = []
    instances.append(str(os.environ['inst_name']))
    ec2.start_instances(InstanceIds=instances)
    print('instance name: ' + os.environ['inst_name'])
    print('started your instances: ' + str(instances))
