# mcraft_svr_aws_cft
Minecraft server using AWS EC2 instance created by CloudFormation stack

## Description
This repository contains an AWS CloudFormation YAML file to create a Minecraft server hosted on an EC2 instance in AWS.
It fully automates the process of creating the requisite IAM roles, Security Groups, and the EC2 instance on which the minecraft server runs.
Optionally an Elastic IP can be passed in to preserve the IP of the server upon start/stop instance.

## Pre-requisites
* You should have your own AWS account
* You should create your own S3 bucket and place the 2 files below in it - see https://minecraft-svr-bkt.s3-us-west-1.amazonaws.com/README.txt for details
  * https://minecraft-svr-bkt.s3-us-west-1.amazonaws.com/minecraft_server.1.16.4.jar - or later version from https://www.minecraft.net/en-us/download/server/
  * https://minecraft-svr-bkt.s3-us-west-1.amazonaws.com/minecraft.service 
* You should understand the costs involved - see https://aws.amazon.com/ec2/pricing/ - a t3a.medium suffices for up to ~5 players 

## Commmand line
The stack can be created in e.g. AWS Cloud9 from the command line as follows: -

- minimal parameters

<code>$ aws cloudformation create-stack --stack-name testMcraftSvr --template-body file://mcraft_cft.yaml --parameters ParameterKey=KeyNameParam,ParameterValue=minecraft-svr ParameterKey=UserDataParam,ParameterValue=$(base64 -w0 mcraft-user-data.txt) --capabilities CAPABILITY_NAMED_IAM</code>

- select a different instance type to host the minecraft server

<code>$ aws cloudformation create-stack --stack-name testMcraftSvr --template-body file://mcraft_cft.yaml --parameters ParameterKey=KeyNameParam,ParameterValue=minecraft-svr ParameterKey=InstanceTypeParam,ParameterValue=t3a.medium ParameterKey=UserDataParam,ParameterValue=$(base64 -w0 mcraft-user-data.txt) --capabilities CAPABILITY_NAMED_IAM</code>

- associate a BYOIP / Elastic IP
 
<code>$ aws cloudformation create-stack --stack-name testMcraftSvr --template-body file://mcraft_cft.yaml --parameters ParameterKey=KeyNameParam,ParameterValue=minecraft-svr ParameterKey=UserDataParam,ParameterValue=$(base64 -w0 mcraft-user-data.txt) ParameterKey=EIPAssocParam,ParameterValue=true ParameterKey=ElasticIpParam,ParameterValue=123.123.123.123 --capabilities CAPABILITY_NAMED_IAM</code>

To update the stack e.g. to change the instance-type POST stack creation, simply replace <code>create-stack</code> with <code>update-stack</code>

## Outputs
Look at the Outputs section of the CFT stack to find the MCraftSvrIpPort which is the IP and port to give to your minecraft squadron buddies!	

## Validation
Here are some ways to check everything worked!
* https://mcsrvstat.us/ - type in the MCraftSvrIpPort (dont forget the :25565 port at end) - after a minute or so, it should show "A Minecraft Server" Players 0/20
* ssh to your instance - type <code>journalctl -f -u minecraft.service</code> - it should show a successfully spawned Minecraft world

## Debugging
Here are some debugging tips
* If the stack fails to create check out the CFT stack Events section - it usually has a good error description
* if the stack succeeds but no Minecraft server is created then check (a) the S3 bucket you are using with the minecraft.service and minecraft server jar file is accessible (b) check versions - the script defaults to 1.16.4 - change this to whatever version you want but make sure the S3 bucket version and mcraft-user-data.txt version ref matches (c) check <code>/var/log/user-data.log</code> and <code>/var/log/cloud-init-output.log</code> to see if any errors occurred - e.g. you may need to change the <code>s3_bkt_dir</code> since S3 bucket names need to be unique.

## Next Steps
Apart from "Have fun!"...
* Leverage the StartEC2Instances and StopEc2Instances lambda fxns with a scheduled cron job so that the minecraft server only runs at certain times (saves cost, and avoids your kid staying up all night "mining", and "making the advancement"!!)
  * get the instance-id from your Minecraft server EC2 instance and pass it in as "inst_name" as an Environment variable to the lambda fxn. Do this for both StartEC2Instances and StopEc2Instances
  * Set up a CloudWatch Events Rule eg <code>0 23 ? * MON-FRI *</code> on StartEC2Instances will start the Instance every weekday at 2300 GMT (3pm PST). <code>0 5 ? * MON-FRI *</code> on StopEC2Instances will stop the instance M-F at 9pm PST
* Get an Elastic IP so that your server IP:port never changes & your kids dont get mad! Go to the EC2 service, click Elastic IP -> Allocate Elastic IP address. You can then pass it in to your create-stack, update-stack as a parameter per above cmd line options. Note that AWS charges a (very small) amount for an EIP when your instance is stopped.
* Save cost. A t3a.medium running eg 8 hrs per day with 1 EIP will cost approx ~$12 / month per https://calculator.s3.amazonaws.com/index.html - you can further reduce this by switching to a spot instance - see https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html 
  * To do this, stop the instance, snapshot your current AMI, then create a new instance based on this AMI - check the Request Spot Instance box then bid e.g. 20% higher than the listed spot price. Be sure to check "persistent request" & interruption behavior = "Stop" (ie NOT "terminate"!)
* Check the server health in Cloudwatch - CPU utilization, Network traffic is built in to the EC2 KPIs. The memory utilization/used/available stats were added via the user-data script in the CloudFormation creation. These appear as "Custom Namespaces" -> "System/Linux" in Cloudwatch Metrics. It is suggested to create a CW dashboard to collect all stats, alarms in 1 place - see https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/create_dashboard.html 

## Strange quirks
Here are some oddities that may baffle you as much as they baffled me: -
* user data in the CloudFormation AWS Console - if you use the console then you cant pass in a file w/ base64 encoding as required - so instead you have to enter all of the user-data bash script inline in the CFT yaml per https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-ec2.html#scenario-ec2-instance-with-vol-and-tags . This is ugly! Hence the reason why I use Cloud9 and pass in the user-data as a maintainable, versionable file instead using <code>ParameterKey=UserDataParam,ParameterValue=$(base64 -w0 mcraft-user-data.txt)</code>
* persistent spot instance request in CFT - couldnt see any options for this in https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html - hence the template simply uses an OnDemand instance

## RGR (Rather Good References)
Here are some killer articles which helped me en-route: -
* https://medium.com/@lanceweber/hosting-your-minecraft-server-on-aws-chapter-1-introduction-syllabus-934db77a0985
* https://medium.com/@sumekenov/how-to-launch-minecraft-server-on-aws-7f4b9f7febf7
* https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-guide.html
* https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html
* https://stackoverflow.com/questions/38195137/passing-userdata-file-to-aws-cloudformation-stack
