import unittest

from moto import mock_iam

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

    def test_no_iam_users_results_in_no_results(self):
        results = inspect(self.dummy_credentials, "eu-west-1")
        self.assertListEqual(results, [], "No IAM users should mean no results are produced")
