import datetime
import os
import json

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def handler(event, _context):
    print(f"handling event: {event}")

    today = datetime.datetime.today()
    thirty_days_from_today = today + datetime.timedelta(30)

    for record in event["Records"]:
        message_body = json.loads(record["body"])

        account_id = message_body["account_id"]
        rule_name = message_body["rule_name"]
        region = message_body["region"]
        inspection_date = message_body["inspection_date"]
        report = message_body["report"]

        table.put_item(
            Item={
                "partition_key": f"{account_id}|{rule_name}",
                "inspection_date": inspection_date,
                "region": region,
                "report": report,
                "ttl": int(thirty_days_from_today.timestamp())
            }
        )

if __name__ == "__main__":
    handler({}, None)
