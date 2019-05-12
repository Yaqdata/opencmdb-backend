import boto3


def get_aws_instances():
    ec2 = boto3.client('ec2')
    return ec2.describe_instances()
