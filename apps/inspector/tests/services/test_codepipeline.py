import unittest
import json

from moto import mock_codepipeline, mock_iam
import boto3

from inspector.services.codepipeline import inspect

def generate_pipeline_structure(*, role_arn, pipeline_type):
    return {
        "name": "my-pipeline",
        "roleArn": role_arn,
        "pipelineType": pipeline_type,
        "stages": [
            {
                "name": "Source",
                "actions": [
                    {
                        "name": "SourceAction",
                        "actionTypeId": {
                            "category": "Source",
                            "owner": "AWS",
                            "provider": "S3",
                            "version": "1"
                        },
                        "configuration": {
                            "S3Bucket": "YOUR_S3_BUCKET",
                            "S3ObjectKey": "YOUR_S3_OBJECT_KEY",
                            "PollForSourceChanges": "false"
                        },
                        "outputArtifacts": [
                            {
                                "name": "SourceOutput"
                            }
                        ],
                        "runOrder": 1
                    }
                ]
            },
            {
                "name": "Build",
                "actions": [
                    {
                        "name": "BuildAction",
                        "actionTypeId": {
                            "category": "Build",
                            "owner": "AWS",
                            "provider": "CodeBuild",
                            "version": "1"
                        },
                        "inputArtifacts": [
                            {
                                "name": "SourceOutput"
                            }
                        ],
                        "outputArtifacts": [
                            {
                                "name": "BuildOutput"
                            }
                        ],
                        "configuration": {
                            "ProjectName": "YOUR_CODEBUILD_PROJECT_NAME"
                        },
                        "runOrder": 1
                    }
                ]
            }
        ],
        "artifactStore": {
            "type": "S3",
            "location": "YOUR_S3_BUCKET"
        }
    }

@mock_codepipeline
@mock_iam
class CodePipelineTests(unittest.TestCase):
    def setUp(self):
        self.dummy_credentials = {
            "AccessKeyId": "testing",
            "SecretAccessKey": "testing",
            "SessionToken": "testing"
        }

    def tearDown(self):
        pass

    def test_no_pipelines_returns_no_results(self):
        results = inspect(self.dummy_credentials, "eu-west-1")
        self.assertListEqual(results, [], "No pipelines should mean no results are produced")

    # TODO: re-enable these two tests when moto supports asserting on the pipelineType

    # def test_v2_pipeline_returns_no_results(self):
    #     iam = boto3.client("iam")
    #     iam.create_role(
    #         RoleName="my-pipeline-role",
    #         AssumeRolePolicyDocument=json.dumps({
    #             "Statement": [
    #                 {
    #                     "Principal": {
    #                         "Service": "codepipeline.amazonaws.com"
    #                     },
    #                     "Action": "sts:AssumeRole",
    #                     "Effect": "Allow"
    #                 }
    #             ]
    #         })
    #     )
    #     role = boto3.resource("iam").Role("my-pipeline-role")
    #     role.load()

    #     codepipeline = boto3.client("codepipeline")
    #     codepipeline.create_pipeline(pipeline=generate_pipeline_structure(role_arn=role.arn, pipeline_type="V2"))

    #     results = inspect(self.dummy_credentials, "eu-west-1")
    #     self.assertListEqual(results, [], "No pipelines should mean no results are produced")

    # def test_v1_pipeline_returns_result(self):
    #     iam = boto3.client("iam")
    #     iam.create_role(
    #         RoleName="my-pipeline-role",
    #         AssumeRolePolicyDocument=json.dumps({
    #             "Statement": [
    #                 {
    #                     "Principal": {
    #                         "Service": "codepipeline.amazonaws.com"
    #                     },
    #                     "Action": "sts:AssumeRole",
    #                     "Effect": "Allow"
    #                 }
    #             ]
    #         })
    #     )
    #     role = boto3.resource("iam").Role("my-pipeline-role")
    #     role.load()

    #     codepipeline = boto3.client("codepipeline")
    #     codepipeline.create_pipeline(pipeline=generate_pipeline_structure(role_arn=role.arn, pipeline_type="V1"))

    #     results = inspect(self.dummy_credentials, "eu-west-1")
    #     self.assertListEqual(
    #         results,
    #         [
    #             {
    #                 "rule_name": "codepipeline_v1_pipeline",
    #                 "report": {
    #                     "message": "CodePipeline of type v1 exists (my-pipeline)",
    #                     "remedy": "Migrate the pipeline to a v2 pipeline.",
    #                     "resource_id": "my-pipeline",
    #                     "region": "eu-west-1"
    #                 }
    #             }
    #         ],
    #         "A v1 pipeline should mean a result is produced"
    #     )
