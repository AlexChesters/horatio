import os
import datetime

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def handler(event, _context):
    print(f"handling event: {event}")

    today = datetime.datetime.today()

    response = table.query(
        IndexName="InspectionDateIndex",
        KeyConditionExpression="inspection_date = :today",
        ExpressionAttributeValues={
            ":today": f"{today.year}-{today.month}-{today.day}"
        }
    )

    print(f"response: {response}")

if __name__ == "__main__":
    handler({}, None)
