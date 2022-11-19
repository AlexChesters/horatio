import boto3

def send_email(body):
    client = boto3.client("ses", region_name="eu-west-1")

    client.send_email(
        Source="horatio@alexchesters.com",
        Destination={
            "ToAddresses": "alex@cheste.rs"
        },
        Message={
            "Subject": {
                "Charset": "UTF-8",
                "Data": "Horatio Daily Report"
            },
            "Body": {
                "Html": {
                    "Charset": "UTF-8",
                    "Data": body
                }
            }
        }
    )
