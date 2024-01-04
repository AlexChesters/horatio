import unittest

from moto import mock_iam
import boto3
from freezegun import freeze_time

from inspector.services.iam import inspect

@mock_iam
class IAMTests(unittest.TestCase):
    def setUp(self):
        self.dummy_credentials = {
            "AccessKeyId": "testing",
            "SecretAccessKey": "testing",
            "SessionToken": "testing"
        }

    def tearDown(self):
        pass

    def test_no_iam_users_returns_no_results(self):
        results = inspect(self.dummy_credentials, "eu-west-1")
        self.assertListEqual(results, [], "No IAM users should mean no results are produced")

    def test_iam_user_without_access_key_returns_no_results(self):
        iam = boto3.resource("iam")
        user = iam.User("some-user")
        user.create()

        results = inspect(self.dummy_credentials, "eu-west-1")
        self.assertListEqual(results, [], "An IAM user without an access key should mean no results are produced")

    def test_iam_user_with_recent_access_key_returns_no_results(self):
        iam = boto3.resource("iam")
        user = iam.User("some-user")
        user.create()
        user.create_access_key_pair()

        results = inspect(self.dummy_credentials, "eu-west-1")
        self.assertListEqual(results, [], "An IAM user with a recent access key should mean no results are produced")

    @freeze_time("2023-05-17", as_kwarg="ft")
    def test_iam_user_with_old_access_key_returns_a_result(self, ft):
        iam = boto3.resource("iam")
        user = iam.User("some-user")
        user.create()
        user.create_access_key_pair()

        ft.move_to("2024-05-17")

        results = inspect(self.dummy_credentials, "eu-west-1")
        self.assertListEqual(
            results,
            [
                {
                    "rule_name": "iam_user_access_key_age",
                    "report": {
                        "message": "IAM user has an access key older than 90 days (366)",
                        "remedy": "Rotate the access key.",
                        "resource_id": "some-user",
                        "region": "eu-west-1"
                    }
                }
            ],
            "An IAM user with an old access key should mean a result is produced"
        )
