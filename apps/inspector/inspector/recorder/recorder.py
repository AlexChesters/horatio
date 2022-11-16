import os
import datetime

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def record(account_id, rule_name, result):
    print(f"recording result {result} for account {account_id}")

    today = datetime.datetime.today()
    thirty_days_from_today = today + datetime.timedelta(30)

    table.put_item(
        Item={
            "partition_key": f"{account_id}|{rule_name}",
            "inspection_date": f"{today.year}-{today.month}-{today.day}",
            "result": result,
            "ttl": int(thirty_days_from_today.timestamp())
        }
    )
