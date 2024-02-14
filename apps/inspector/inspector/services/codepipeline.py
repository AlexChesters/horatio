import boto3
from aws_lambda_powertools import Logger

# from inspector.utils.flatten import flatten

logger = Logger()

def find_v1_pipelines(_client, _region):
    results = []

    return results

def inspect(credentials, region):
    logger.info(f"inspecting codepipeline resources in {region}")

    results = []

    client = boto3.client(
        "codepipeline",
        region_name=region,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"]
    )

    results.extend(find_v1_pipelines(client, region))

    return results
