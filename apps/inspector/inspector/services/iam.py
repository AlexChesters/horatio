from datetime import datetime, timezone

import boto3

from inspector.utils.flatten import flatten

def find_access_keys_of_old_age(client):
    results = []

    users_paginator = client.get_paginator("list_users")
    users_results = flatten([
        result["Users"]
        for result in users_paginator.paginate()
    ])

    for user in users_results:
        access_keys_paginator = client.get_paginator("list_access_keys")
        access_keys_results = flatten([
            result["AccessKeyMetadata"]
            for result in access_keys_paginator.paginate(UserName=user["UserName"])
        ])

        for access_key in access_keys_results:
            access_key_create_date = access_key["CreateDate"]
            now = datetime.now(timezone.utc)
            delta = now - access_key_create_date

            if delta.days > 30:
                results.append({
                    "rule_name": "iam_user_access_key_age",
                    "report": {
                        "message": "IAM user has an access key older than 30 days",
                        "remedy": "Rotate the access key.",
                        "resource_id": user["UserName"]
                    }
                })
            print(f"access key is {delta.days} days old")

    return results

def inspect(credentials, _region):
    print("inspecting iam resources")

    results = []

    client = boto3.client(
        "iam",
        region_name="us-east-1",
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"]
    )

    results.extend(find_access_keys_of_old_age(client))

    return results
