import boto3

from inspector.utils.flatten import flatten

def verify_budgets_exist(client, region, account_id):
    results = []

    paginator = client.get_paginator("describe_budget_notifications_for_account")
    print(f"analysing notifications for account {account_id}")

    notifications_for_account = flatten([
        result.get("BudgetNotificationsForAccount", [])
        for result in paginator.paginate(AccountId=account_id)
    ])

    account_has_notification_for_forecast = False
    account_has_notification_for_actual = False

    for notifications in notifications_for_account:
        for notification in notifications.get("Notifications", []):
            if notification["NotificationType"] == "ACTUAL":
                account_has_notification_for_actual = True
            elif notification["NotificationType"] == "FORECASTED":
                account_has_notification_for_forecast = True

    if not account_has_notification_for_forecast:
        results.append({
            "rule_name": "forecast_budget_with_notification",
            "report": {
                "message": "No forecast budget with an notification exists",
                "remedy": "Create a forecast budget with an associated notification",
                "resource_id": account_id,
                "region": region
            }
        })

    if not account_has_notification_for_actual:
        results.append({
            "rule_name": "actual_budget_with_notification",
            "report": {
                "message": "No actual budget with an notification exists",
                "remedy": "Create a actual budget with an associated notification",
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
