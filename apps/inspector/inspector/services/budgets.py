import boto3

from inspector.utils.flatten import flatten

def verify_budgets_exist(client, region, account_id):
    results = []

    paginator = client.get_paginator("describe_budget_actions_for_account")
    print(f"analysing actions for account {account_id}")

    actions = flatten([
        result.get("Actions", [])
        for result in paginator.paginate(AccountId=account_id)
    ])

    account_has_action_for_forecast = False
    account_has_action_for_actual = False

    print(f"analysing actions: {actions}")
    for action in actions:
        if action["NotificationType"] == "ACTUAL":
            account_has_action_for_actual = True
        elif action["NotificationType"] == "FORECASTED":
            account_has_action_for_forecast = True

    if not account_has_action_for_forecast:
        results.append({
            "rule_name": "forecast_budget_with_action",
            "report": {
                "message": "No forecast budget with an action exists",
                "remedy": "Create a forecast budget with an associated action",
                "resource_id": account_id,
                "region": region
            }
        })

    if not account_has_action_for_actual:
        results.append({
            "rule_name": "actual_budget_with_action",
            "report": {
                "message": "No actual budget with an action exists",
                "remedy": "Create a actual budget with an associated action",
                "resource_id": account_id,
                "region": region
            }
        })

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
