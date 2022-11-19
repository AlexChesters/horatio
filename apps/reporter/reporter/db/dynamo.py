import datetime

import boto3

from reporter.utils.flatten import flatten
from reporter.utils.dynamo import deserialise

client = boto3.client("dynamodb")

def get_todays_data():
    today = datetime.datetime.today()

    paginator = client.get_paginator("query")

    results = paginator.paginate(
        TableName=os.environ["TABLE_NAME"],
        IndexName="InspectionDateIndex",
        Select="SPECIFIC_ATTRIBUTES",
        ProjectionExpression="report",
        KeyConditionExpression="inspection_date = :today",
        ExpressionAttributeValues={
            ":today": {
                "S": f"{today.year}-{today.month}-{today.day}"
            }
        }
    )

    results = flatten([result["Items"] for result in results])

    return map(lambda result: deserialise(result), results)
