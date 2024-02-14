import boto3
from aws_lambda_powertools import Logger

from inspector.utils.flatten import flatten

logger = Logger()

def find_v1_pipelines(client, region):
    results = []

    paginator = client.get_paginator("list_pipelines")
    list_pipeline_results = flatten([
        result["pipelines"]
        for result in paginator.paginate()
    ])

    for result in list_pipeline_results:
        if result["pipelineType"] == "V1":
            pipeline_name = result["name"]
            results.append({
                "rule_name": "codepipeline_v1_pipeline",
                "report": {
                    "message": f"CodePipeline of type v1 exists ({pipeline_name})",
                    "remedy": "Migrate the pipeline to a v2 pipeline.",
                    "resource_id": pipeline_name,
                    "region": region
                }
            })

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
