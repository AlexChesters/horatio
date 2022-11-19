import datetime

import boto3

def send_email(body):
    client = boto3.client("ses", region_name="eu-west-1")

    today = datetime.datetime.today()

    client.send_email(
        Source="horatio@alexchesters.com",
        Destination={
            "ToAddresses": ["alex@cheste.rs"]
        },
        Message={
            "Subject": {
                "Charset": "UTF-8",
                "Data": f"Horatio Report - {today.day}/{today.month}/{today.year}"
            },
            "Body": {
                "Html": {
                    "Charset": "UTF-8",
                    "Data": body
                }
            }
        }
    )
