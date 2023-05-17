import unittest

from moto import mock_iam
import boto3

from inspector.services.iam import inspect

@mock_iam
class IAMTestsTests(unittest.TestCase):
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
