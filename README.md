# mcraft_svr_aws_cft
Minecraft server using AWS EC2 instance created by CloudFormation stack

## Description
This repository contains an AWS CloudFormation YAML file to create a Minecraft server hosted on an EC2 instance in AWS.
It fully automates the process of creating the requisite IAM roles, Security Groups, and the EC2 instance on which the minecraft server runs.
Optionally an Elastic IP can be passed in to preserve the IP of the server upon start/stop instance.

## Commmand line
The stack can be created in e.g. AWS Cloud9 from the command line as follows: -

- minimal parameters
$ aws cloudformation create-stack --stack-name testMcraftSvr --template-body file://mcraft_cft.yaml --parameters ParameterKey=KeyNameParam,ParameterValue=minecraft-svr ParameterKey=UserDataParam,ParameterValue=$(base64 -w0 mcraft-user-data.txt) --capabilities CAPABILITY_NAMED_IAM

- select a different instance type to host the minecraft server
$ aws cloudformation create-stack --stack-name testMcraftSvr --template-body file://mcraft_cft.yaml --parameters ParameterKey=KeyNameParam,ParameterValue=minecraft-svr ParameterKey=InstanceTypeParam,ParameterValue=t3a.medium ParameterKey=UserDataParam,ParameterValue=$(base64 -w0 mcraft-user-data.txt) --capabilities CAPABILITY_NAMED_IAM

- associate a BYOIP / Elastic IP 
aws cloudformation create-stack --stack-name testMcraftSvr --template-body file://mcraft_cft.yaml --parameters ParameterKey=KeyNameParam,ParameterValue=minecraft-svr ParameterKey=UserDataParam,ParameterValue=$(base64 -w0 mcraft-user-data.txt) ParameterKey=EIPAssocParam,ParameterValue=true ParameterKey=ElasticIpParam,ParameterValue=123.123.123.123 --capabilities CAPABILITY_NAMED_IAM

## Outputs
Look at the Outputs section of the CFT stack to find the MCraftSvrIpPort which is the IP and port to give to your minecraft squadron buddies!	
