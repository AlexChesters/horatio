import datetime
import os
import json

import boto3
from aws_lambda_powertools import Logger

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

logger = Logger()

@logger.inject_lambda_context(log_event=True)
def handler(event, _context):
    today = datetime.datetime.today()
    thirty_days_from_today = today + datetime.timedelta(30)

    for record in event["Records"]:
        message_body = json.loads(record["body"])

        account_id = message_body["account_id"]
        rule_name = message_body["rule_name"]
        inspection_date = message_body["inspection_date"]
        report = message_body["report"]

        table.put_item(
            Item={
                "partition_key": f"{account_id}|{rule_name}",
                "inspection_date": inspection_date,
                "report": report,
                "ttl": int(thirty_days_from_today.timestamp())
            }
        )

if __name__ == "__main__":
    handler({}, None)
