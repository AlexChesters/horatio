import boto3
from aws_lambda_powertools import Logger

from inspector.utils.flatten import flatten

logger = Logger()

def find_deprecated_codebuild_images(client, region):
    results = []

    current_images = client.list_curated_environment_images()
    current_image_names = [
        image["name"]
        for platform in current_images["platforms"]
        for language in platform["languages"]
        for image in language["images"]
    ]

    list_projects_paginator = client.get_paginator("list_projects")
    list_projects_results = flatten([
        result["projects"]
        for result in list_projects_paginator.paginate()
    ])

    if list_projects_results:
        projects = client.batch_get_projects(names=list_projects_results)["projects"]

        for project in projects:
            image_name = project["environment"]["image"]
            if image_name.startswith("aws/") and image_name not in current_image_names:
                results.append({
                    "rule_name": "deprecated_codebuild_image",
                    "report": {
                        "message": "CodeBuild project is using a deprecated image",
                        "remedy": "Update the project to use a current image",
                        "resource_id": project["name"],
                        "region": region
                    }
                })

    return results

def inspect(credentials, region):
    logger.info(f"inspecting codebuild resources in {region}")

    results = []

    client = boto3.client(
        "codebuild",
        region_name=region,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"]
    )

    results.extend(find_deprecated_codebuild_images(client, region))

    return results
