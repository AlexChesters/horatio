import boto3
from aws_lambda_powertools import Logger

from inspector.utils.flatten import flatten

logger = Logger()

def find_topics_without_subscriptions(client, region):
    results = []

    topics_results = flatten([
        result["Topics"]
        for result in client.get_paginator("list_topics").paginate()
    ])

    for topic in topics_results:
        subscriptions_results = flatten([
            result["Subscriptions"]
            for result in client.get_paginator("list_subscriptions_by_topic").paginate(TopicArn=topic["TopicArn"])
        ])

        if not subscriptions_results:
            results.append({
                "rule_name": "sns_topic_without_subscriptions",
                "report": {
                    "message": "SNS Topic exists without any subscriptions",
                    "remedy": "Add subscriptions if required, otherwise delete the topic.",
                    "resource_id": topic["TopicArn"],
                    "region": region
                }
            })

    return results

def find_topics_with_unconfirmed_subscriptions(client, region):
    results = []

    subscriptions_results = flatten([
        result["Subscriptions"]
        for result in client.get_paginator("list_subscriptions").paginate()
    ])

    for subscription in subscriptions_results:
        if subscription["SubscriptionArn"] == "PendingConfirmation":
            results.append({
                "rule_name": "sns_topic_with_unconfirmed_subscriptions",
                "report": {
                    "message": "SNS Topic exists with unconfirmed subscription(s)",
                    "remedy": "Confirm the subscription(s).",
                    "resource_id": subscription["TopicArn"],
                    "region": region
                }
            })

    return results

def inspect(credentials, region):
    logger.info(f"inspecting sns resources in {region}")

    results = []

    client = boto3.client(
        "sns",
        region_name=region,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"]
    )

    results.extend(find_topics_without_subscriptions(client, region))
    results.extend(find_topics_with_unconfirmed_subscriptions(client, region))

    return results
