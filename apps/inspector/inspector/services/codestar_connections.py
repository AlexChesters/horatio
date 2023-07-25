import boto3
from aws_lambda_powertools import Logger

from inspector.utils.flatten import flatten
from inspector.utils.paginate import paginate

logger = Logger()

def find_incomplete_codestar_connections(client, region):
    results = []

    list_connections_results = flatten(paginate(client.list_connections, "Connections"))

    for connection in list_connections_results:
        if connection["ConnectionStatus"] != "AVAILABLE":
            results.append({
                "rule_name": "incomplete_codestar_connection",
                "report": {
                    "message": "Incomplete CodeStar Connection exists",
                    "remedy": "Fix or delete the connection.",
                    "resource_id": connection["ConnectionArn"],
                    "region": region
                }
            })

    return results

def inspect(credentials, region):
    logger.info(f"inspecting codestar connection resources in {region}")

    results = []

    client = boto3.client(
        "codestar-connections",
        region_name=region,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"]
    )

    results.extend(find_incomplete_codestar_connections(client, region))

    return results
