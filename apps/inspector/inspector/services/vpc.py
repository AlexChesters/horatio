import boto3

def inspect(credentials):
    client = boto3.client(
        "ec2",
        region_name="eu-west-1",
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"]
    )

    paginator = client.get_paginator("describe_vpcs")

    vpc_results = [
        result["Vpcs"]
        for result in paginator.paginate()
    ]

    for vpc in vpc_results:
        print(f"found vpc: {vpc}")
