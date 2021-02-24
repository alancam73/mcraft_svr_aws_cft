import boto3
import os

# change this to your AWS region
region = 'us-west-1'
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    instances = []
    instances.append(str(os.environ['inst_name']))
    ec2.stop_instances(InstanceIds=instances)
    print('instance name: ' + os.environ['inst_name'])
    print('stopped your instances: ' + str(instances))
