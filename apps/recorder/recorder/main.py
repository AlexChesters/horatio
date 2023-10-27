import datetime
import os
import json

import boto3
from aws_lambda_powertools import Logger, Tracer, Metrics, single_metric
from aws_lambda_powertools.metrics import MetricUnit

logger = Logger()
tracer = Tracer()
metrics = Metrics()

@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def handler(event, _context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["TABLE_NAME"])

    today = datetime.datetime.today()
    one_year_from_today = today + datetime.timedelta(365)

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
                "ttl": int(one_year_from_today.timestamp())
            }
        )

        with single_metric(name="RecordedMessage", unit=MetricUnit.Count, value=1) as metric:
            metric.add_dimension(name="RuleName", value=rule_name)
            metric.add_dimension(name="AccountID", value=account_id)

if __name__ == "__main__":
    handler({}, None)
