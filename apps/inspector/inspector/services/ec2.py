import boto3

def find_packer_key_pairs(client, region):
    results = []

    key_pair_results = client.describe_key_pairs()

    for key_pair in key_pair_results["KeyPairs"]:
        print(f"found key pair: {key_pair['KeyName']}")
        if key_pair["KeyName"].startswith("packer_"):
            results.append({
                "rule_name": "packer_key_pair_exists",
                "report": {
                    "message": "Packer key pair exists in account",
                    "remedy": "Delete the packer key pair.",
                    "resource_id": key_pair["KeyName"],
                    "region": region
                }
            })

    return results

def inspect(credentials, region):
    print(f"inspecting ec2 resources in {region}")

    results = []

    client = boto3.client(
        "ec2",
        region_name=region,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"]
    )

    results.extend(find_packer_key_pairs(client, region))

    return results
