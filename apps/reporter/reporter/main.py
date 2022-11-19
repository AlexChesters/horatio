import os
import datetime

import boto3

from reporter.utils.flatten import flatten

client = boto3.client("dynamodb")

def handler(event, _context):
    print(f"handling event: {event}")

    today = datetime.datetime.today()

    paginator = client.get_paginator("query")

    results = paginator.paginate(
        TableName=os.environ["TABLE_NAME"],
        IndexName="InspectionDateIndex",
        Select="ALL_ATTRIBUTES",
        KeyConditionExpression="inspection_date = :today",
        ExpressionAttributeValues={
            ":today": {
                "S": f"{today.year}-{today.month}-{today.day}"
            }
        }
    )

    results = flatten([result["Items"] for result in results])

    print(f"results: {results}")

if __name__ == "__main__":
    handler({}, None)
