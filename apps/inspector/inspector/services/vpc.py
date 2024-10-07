import boto3
from aws_lambda_powertools import Logger

from inspector.utils.flatten import flatten

logger = Logger()

def find_default_vpcs(client, region):
    results = []

    paginator = client.get_paginator("describe_vpcs")

    vpc_results = flatten([
        result["Vpcs"]
        for result in paginator.paginate()
    ])

    logger.debug(f"found {len(vpc_results)} vpcs in {region}")

    for vpc in vpc_results:
        vpc_id = vpc["VpcId"]
        logger.debug(f"vpc id: {vpc_id}")

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

def inspect(credentials, region):
    logger.info(f"inspecting vpc resources in {region}")

    results = []

    client = boto3.client(
        "ec2",
        region_name=region,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"]
    )

    results.extend(find_default_vpcs(client, region))

    return results
