from datetime import datetime, timezone

import boto3
from aws_lambda_powertools import Logger

from inspector.utils.flatten import flatten

logger = Logger()

def find_packer_key_pairs(client, region):
    results = []

    key_pair_results = client.describe_key_pairs()

    for key_pair in key_pair_results["KeyPairs"]:
        if key_pair["KeyName"].startswith("packer_"):
            now = datetime.now(timezone.utc)
            delta = now - key_pair["CreateTime"]

            if delta.total_seconds() / 3600 > 30:
                results.append({
                    "rule_name": "packer_key_pair_exists",
                    "report": {
                        "message": "Packer key pair exists in account",
                        "remedy": "Delete the packer key pair.",
                        "resource_id": key_pair["KeyName"],
                        "region": region
                    }
                })

    return results

def find_stopped_instances(client, region):
    results = []

    instances_results = flatten([
        result["Reservations"]
        for result in client.get_paginator("describe_instances").paginate()
    ])

    for result in instances_results:
        for instance in result["Instances"]:
            if instance["State"]["Name"] == "stopped":
                results.append({
                    "rule_name": "instance_stopped",
                    "report": {
                        "message": "An EC2 instance in the stopped state",
                        "remedy": "Terminate or restart the instance.",
                        "resource_id": instance["InstanceId"],
                        "region": region
                    }
                })

    return results

def inspect(credentials, region):
    logger.info(f"inspecting ec2 resources in {region}")

    results = []

    client = boto3.client(
        "ec2",
        region_name=region,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"]
    )

    results.extend(find_packer_key_pairs(client, region))
    results.extend(find_stopped_instances(client, region))

    return results
