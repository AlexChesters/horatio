import boto3

from inspector.utils.flatten import flatten

def verify_budget_stack_exists(client, region):
    results = []

    paginator = client.get_paginator("list_stacks")

    stack_results = flatten([
        result["StackSummaries"]
        for result in paginator.paginate()
    ])

    budget_stack_exists = False

    for stack in stack_results:
        if stack["StackName"] == "budget":
            budget_stack_exists = True

    if not budget_stack_exists:
        results.append({
            "rule_name": "budget",
            "report": {
                "message": "Budget stack does not exist in account",
                "remedy": "Create a budget stack in the account.",
                "resource_id": None,
                "region": region
            }
        })

    return results

def inspect(credentials, region):
    print(f"inspecting cloudformation resources in {region}")

    results = []

    client = boto3.client(
        "cloudformation",
        region_name=region,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"]
    )

    results.extend(verify_budget_stack_exists(client, region))

    return results
