import boto3
from aws_lambda_powertools import Logger

from inspector.utils.flatten import flatten
from inspector.utils.assume_role import assume_role

logger = Logger()

def get_accounts_to_inspect():
    list_accounts_credentials = assume_role("arn:aws:iam::008356366354:role/horatio-list-accounts-role")

    cloudformation = boto3.client(
        "cloudformation",
        aws_access_key_id=list_accounts_credentials["AccessKeyId"],
        aws_secret_access_key=list_accounts_credentials["SecretAccessKey"],
        aws_session_token=list_accounts_credentials["SessionToken"]
    )
    list_stack_instances_paginator = cloudformation.get_paginator("list_stack_instances")

    stack_instances = [
        result["Summaries"]
        for result in list_stack_instances_paginator.paginate(
            StackSetName="horatio-inspection-role",
            CallAs="SELF"
        )
    ]

    stack_instance_accounts = [instance["Account"] for instance in flatten(stack_instances)]

    return stack_instance_accounts
