import unittest

from moto import mock_ec2
import boto3

from inspector.services.ec2 import inspect

@mock_ec2
class EC2Tests(unittest.TestCase):
    def setUp(self):
        self.dummy_credentials = {
            "AccessKeyId": "testing",
            "SecretAccessKey": "testing",
            "SessionToken": "testing"
        }

    def tearDown(self):
        pass

    def test_no_key_pairs_results_in_no_results(self):
        results = inspect(self.dummy_credentials, "eu-west-1")
        self.assertListEqual(results, [], "No key pairs should mean no results are produced")

    def test_non_packer_key_pairs_results_in_no_results(self):
        ec2 = boto3.resource("ec2")
        ec2.create_key_pair(
            KeyName="some-keypair"
        )

        results = inspect(self.dummy_credentials, "eu-west-1")
        self.assertListEqual(results, [], "No key pairs should mean no results are produced")

    def test_packer_key_pairs_returns_a_result(self):
        ec2 = boto3.resource("ec2")
        ec2.create_key_pair(
            KeyName="packer_abc123"
        )

        results = inspect(self.dummy_credentials, "eu-west-1")
        self.assertListEqual(
            results,
            [
                {
                "rule_name": "packer_key_pair_exists",
                "report": {
                    "message": "Packer key pair exists in account",
                    "remedy": "Delete the packer key pair.",
                    "resource_id": "packer_abc123",
                    "region": "eu-west-1"
                }
            }
            ],
            "A packer key pair should mean a result is produced"
        )