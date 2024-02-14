import os
import datetime
import json

import boto3
from aws_lambda_powertools import Logger, Tracer, Metrics, single_metric
from aws_lambda_powertools.metrics import MetricUnit

from inspector.services import budgets, vpc, ec2, iam, sns, codestar_connections, codepipeline

from inspector.utils.flatten import flatten

MANAGEMENT_ACCOUNT_ID = "008356366354"

SERVICE_MAP = {
    "VPC": vpc,
    "EC2": ec2,
    "BUDGETS": budgets,
    "IAM": iam,
    "SNS": sns,
    "CODESTAR_CONNECTIONS": codestar_connections,
    "CODEPIPELINE": codepipeline
}

logger = Logger()
tracer = Tracer()
metrics = Metrics()

def assume_role(role_arn):
    sts_client = boto3.client("sts")
    assumed_role_object = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="horatio-inspector"
    )
    return assumed_role_object["Credentials"]

@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def handler(event, _context):
    sqs = boto3.resource("sqs")
    queue = sqs.Queue(os.environ["QUEUE_URL"])
    service_name = event["SERVICE"]

    service = SERVICE_MAP[service_name]

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
        account_status = account["Status"]

        if account_status == "SUSPENDED":
            logger.info(f"ignoring account {account_name} as it is suspended")
            continue

        logger.info(f"processing account {account_name} ({account_id})")

        if account_id == MANAGEMENT_ACCOUNT_ID:
            logger.info(f"{account_name} is management account, skipping")
            continue

        target_account_credentials = assume_role(f"arn:aws:iam::{account_id}:role/horatio-inspection-target-account-role")

        for region in event["REGIONS"]:
            results = service.inspect(target_account_credentials, region)

            for result in results:
                today = datetime.datetime.today()

                report = result["report"]
                report["account_id"] = account_id

                rule_name = result["rule_name"]

                logger.info(f"sending message to queue {account_id}|{rule_name}")

                queue.send_message(
                    MessageBody=json.dumps({
                        "account_id": account_id,
                        "rule_name": rule_name,
                        "inspection_date": f"{today.year}-{today.month}-{today.day}",
                        "report": report
                    })
                )

                with single_metric(name="Finding", unit=MetricUnit.Count, value=1) as metric:
                    metric.add_dimension(name="ServiceName", value=service_name)
                    metric.add_dimension(name="RuleName", value=rule_name)
                    metric.add_dimension(name="AccountID", value=account_id)
