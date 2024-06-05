import os
import datetime
import json

import boto3
from aws_lambda_powertools import Logger, Tracer, Metrics, single_metric
from aws_lambda_powertools.metrics import MetricUnit

from inspector.services import budgets, vpc, ec2, iam, sns, codestar_connections, codepipeline
from inspector.accounts.get_accounts_to_inspect import get_accounts_to_inspect
from inspector.utils.assume_role import assume_role

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

@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def handler(event, _context):
    sqs = boto3.resource("sqs")
    queue = sqs.Queue(os.environ["QUEUE_URL"])
    service_name = event["SERVICE"]

    service = SERVICE_MAP[service_name]

    accounts_to_inspect = get_accounts_to_inspect()

    for account_id in accounts_to_inspect:
        logger.info(f"processing account {account_id}")

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
