import boto3

from inspector.utils.flatten import flatten

def inspect(credentials, region):
    results = []

    client = boto3.client(
        "ec2",
        region_name=region,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"]
    )

    paginator = client.get_paginator("describe_vpcs")

    vpc_results = flatten([
        result["Vpcs"]
        for result in paginator.paginate()
    ])

    for vpc in vpc_results:
        if vpc["IsDefault"]:
            results.append({
                "rule_name": "default_vpc_exists",
                "report": {
                    "message": "Default VPC exists in account",
                    "remedy": "Delete the default VPC, replace with a custom one if a VPC is needed.",
                    "resource_id": vpc["VpcId"],
                    "region": region
                }
            })

    return results
