import os
import datetime
import json

import boto3

sqs = boto3.resource("sqs")
queue = sqs.Queue(os.environ["QUEUE_URL"])

def record(account_id, rule_name, result):
    print(f"recording result {result} for account {account_id}")

    today = datetime.datetime.today()

    queue.send_message(
        MessageBody=json.dumps({
            "account_id": account_id,
            "rule_name": rule_name,
            "inspection_date": f"{today.year}-{today.month}-{today.day}",
            "result": result
        })
    )
