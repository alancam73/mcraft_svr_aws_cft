# mcraft_svr_aws_cft
Minecraft server using AWS EC2 instance created by CloudFormation stack

## Description
This repository contains an AWS CloudFormation YAML file to create a Minecraft server hosted on an EC2 instance in AWS.
It fully automates the process of creating the requisite IAM roles, Security Groups, and the EC2 instance on which the minecraft server runs.
Optionally an Elastic IP can be passed in to preserve the IP of the server upon start/stop instance.

## Commmand line
The stack can be created in e.g. AWS Cloud9 from the command line as follows: -

- minimal parameters

<code>$ aws cloudformation create-stack --stack-name testMcraftSvr --template-body file://mcraft_cft.yaml --parameters ParameterKey=KeyNameParam,ParameterValue=minecraft-svr ParameterKey=UserDataParam,ParameterValue=$(base64 -w0 mcraft-user-data.txt) --capabilities CAPABILITY_NAMED_IAM</code>

- select a different instance type to host the minecraft server

<code>$ aws cloudformation create-stack --stack-name testMcraftSvr --template-body file://mcraft_cft.yaml --parameters ParameterKey=KeyNameParam,ParameterValue=minecraft-svr ParameterKey=InstanceTypeParam,ParameterValue=t3a.medium ParameterKey=UserDataParam,ParameterValue=$(base64 -w0 mcraft-user-data.txt) --capabilities CAPABILITY_NAMED_IAM</code>

- associate a BYOIP / Elastic IP
 
<code>$ aws cloudformation create-stack --stack-name testMcraftSvr --template-body file://mcraft_cft.yaml --parameters ParameterKey=KeyNameParam,ParameterValue=minecraft-svr ParameterKey=UserDataParam,ParameterValue=$(base64 -w0 mcraft-user-data.txt) ParameterKey=EIPAssocParam,ParameterValue=true ParameterKey=ElasticIpParam,ParameterValue=123.123.123.123 --capabilities CAPABILITY_NAMED_IAM</code>

## Outputs
Look at the Outputs section of the CFT stack to find the MCraftSvrIpPort which is the IP and port to give to your minecraft squadron buddies!	

## Validation
Here are some ways to check everything worked!
* https://mcsrvstat.us/ - type in the MCraftSvrIpPort (dont forget the :25565 port at end) - after a minute or so, it should show "A Minecraft Server" Players 0/20
* ssh to your instance - type <pre>journalctl -f -u minecraft.service</pre> - it should show a successfully spawned Minecraft world

## Debugging
Here are some debugging tips
* If the stack fails to create check out the CFT stack Events section - it usually has a good error description
* if the stack succeeds but no Minecraft server is created then check (a) the S3 bucket you are using with the minecraft.service and minecraft server jar file is accessible (b) check versions - the script defaults to 1.16.4 - change this to whatever version you want but make sure the S3 bucket version and mcraft-user-data.txt version ref matches (c) check <code>/var/log/user-data.log</code> and <pre>/var/log/cloud-init-output.log</pre> to see if any errors occurred - e.g. you may need to change the <pre>s3_bkt_dir</pre> since S3 bucket names need to be unique.

