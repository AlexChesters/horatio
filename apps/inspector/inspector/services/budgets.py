import boto3

from inspector.utils.flatten import flatten

def verify_budgets_exist(client, _region, account_id):
    results = []

    paginator = client.get_paginator("describe_budgets")

    budgets = flatten([
        result["Budgets"]
        for result in paginator.paginate(AccountId=account_id)
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

    account_id = boto3.client(
        "sts",
        region_name=region,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"]
    ).get_caller_identity().get("Account")

    results.extend(verify_budgets_exist(client, region, account_id))

    return results
