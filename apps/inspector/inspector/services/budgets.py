import boto3

from inspector.utils.flatten import flatten

def verify_budgets_exist(client, _region):
    results = []

    paginator = client.get_paginator("describe_budgets")

    budgets = flatten([
        result["Budgets"]
        for result in paginator.paginate()
    ])

    for budget in budgets:
        print(f"budget: {budget}")

    return results

def inspect(credentials, region):
    print(f"inspecting budget resources in {region}")

    results = []

    client = boto3.client(
        "budgets",
        region_name=region,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"]
    )

    results.extend(verify_budgets_exist(client, region))

    return results
