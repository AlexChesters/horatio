import unittest

from moto import mock_sns
from moto.core import DEFAULT_ACCOUNT_ID as MOTO_DEFAULT_ACCOUNT_ID
import boto3

from inspector.services.sns import inspect

@mock_sns
class SNSTests(unittest.TestCase):
    def setUp(self):
        self.dummy_credentials = {
            "AccessKeyId": "testing",
            "SecretAccessKey": "testing",
            "SessionToken": "testing"
        }

    def tearDown(self):
        pass

    def test_sns_topic_with_no_subscriptions_returns_a_result(self):
        sns = boto3.client("sns")
        sns.create_topic(
            Name="my-topic"
        )

        results = inspect(self.dummy_credentials, "eu-west-1")

        self.assertListEqual(
            results,
            [
                {
                    "rule_name": "sns_topic_without_subscriptions",
                    "report": {
                        "message": "SNS Topic exists without any subscriptions",
                        "remedy": "Add subscriptions if required, otherwise delete the topic.",
                        "resource_id": f"arn:aws:sns:eu-west-1:{MOTO_DEFAULT_ACCOUNT_ID}:my-topic",
                        "region": "eu-west-1"
                    }
                }
            ],
            "An SNS topic with no subscriptions should mean a result is produced"
        )
