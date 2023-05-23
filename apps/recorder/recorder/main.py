import datetime
import os
import json

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer

logger = Logger()
tracer = Tracer()

@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def handler(event, _context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["TABLE_NAME"])

    today = datetime.datetime.today()
    thirty_days_from_today = today + datetime.timedelta(30)

    for record in event["Records"]:
        message_body = json.loads(record["body"])

        account_id = message_body["account_id"]
        rule_name = message_body["rule_name"]
        inspection_date = message_body["inspection_date"]
        report = message_body["report"]
        resource_id = report["resource_id"]

        table.put_item(
            Item={
                "partition_key": f"{account_id}|{rule_name}|{resource_id}",
                "inspection_date": inspection_date,
                "report": report,
                "ttl": int(thirty_days_from_today.timestamp())
            }
        )

if __name__ == "__main__":
    handler({}, None)
