import os
import datetime
import json

import boto3

from inspector.services import vpc

from inspector.utils.flatten import flatten

MANAGEMENT_ACCOUNT_ID = "008356366354"

SERVICE_MAP = {
    "VPC": vpc
}

REGIONS = ["eu-west-1", "eu-west-2", "us-east-1"]

sqs = boto3.resource("sqs")
queue = sqs.Queue(os.environ["QUEUE_URL"])

def assume_role(role_arn):
    sts_client = boto3.client("sts")
    assumed_role_object = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="horatio-inspector"
    )
    return assumed_role_object["Credentials"]

def handler(event, _context):
    print(f"handling event: {event}")

    service = SERVICE_MAP[event["SERVICE"]]

    list_accounts_credentials = assume_role("arn:aws:iam::008356366354:role/horatio-list-accounts-role")

    organisations_client = boto3.client(
        "organizations",
        aws_access_key_id=list_accounts_credentials["AccessKeyId"],
        aws_secret_access_key=list_accounts_credentials["SecretAccessKey"],
        aws_session_token=list_accounts_credentials["SessionToken"]
    )
    organisation_accounts_paginator = organisations_client.get_paginator("list_accounts")

    organisation_accounts_results = [
        result["Accounts"]
        for result in organisation_accounts_paginator.paginate()
    ]

    organisation_accounts = flatten(organisation_accounts_results)

    for account in organisation_accounts:
        account_id = str(account["Id"])
        account_name = account["Name"]

        print(f"processing account {account_name} ({account_id})")

        if account_id == MANAGEMENT_ACCOUNT_ID:
            print(f"{account_name} is management account, skipping")
            continue

        target_account_credentials = assume_role(f"arn:aws:iam::{account_id}:role/horatio-inspection-target-account-role")

        for region in REGIONS:
            results = service.inspect(target_account_credentials, region)

            for result in results:
                today = datetime.datetime.today()

                report = result["report"]
                report["account_id"] = account_id

                queue.send_message(
                    MessageBody=json.dumps({
                        "account_id": account_id,
                        "rule_name": result["rule_name"],
                        "region": region,
                        "inspection_date": f"{today.year}-{today.month}-{today.day}",
                        "report": report
                    })
                )

if __name__ == "__main__":
    handler({}, None)
