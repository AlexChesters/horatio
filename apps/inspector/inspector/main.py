import boto3

from inspector.services import vpc

def flatten(lst):
    return [item for sublist in lst for item in sublist]

def assume_role(role_arn):
    sts_client = boto3.client("sts")
    assumed_role_object = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="horatio-inspector"
    )
    return assumed_role_object["Credentials"]

def handler(event, _context):
    print(f"handling event: {event}")

    list_accounts_credentials = assume_role("arn:aws:iam::008356366354:role/horatio-list-accounts-role")

    organisations_client = boto3.client(
        "organizations",
        aws_access_key_id=list_accounts_credentials["AccessKeyId"],
        aws_secret_access_key=list_accounts_credentials["SecretAccessKey"],
        aws_session_token=list_accounts_credentials["SessionToken"]
    )
    organisation_accounts_paginator = organisations_client.get_paginator("list_accounts")

    organisation_accounts_results = [
        result["Accounts"]
        for result in organisation_accounts_paginator.paginate()
    ]

    organisation_accounts = flatten(organisation_accounts_results)

    for account in organisation_accounts:
        account_id = str(account["Id"])
        account_name = account["Name"]

        print(f"processing account {account_name} ({account_id})")

        target_account_credentials = assume_role(f"arn:aws:iam::{account_id}:role/horatio-inspection-target-account-role")
        vpc.inspect(target_account_credentials)

if __name__ == "__main__":
    handler({}, None)
