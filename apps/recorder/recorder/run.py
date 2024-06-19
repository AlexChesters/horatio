from dataclasses import dataclass

from recorder import main

@dataclass
class LambdaContext:
    function_name: str = "test"
    memory_limit_in_mb: int = 128
    invoked_function_arn: str = "arn:aws:lambda:eu-west-1:809313241:function:test"
    aws_request_id: str = "52fdfc07-2182-154f-163f-5f0f9a621d72"

event = {
    "Records": [
        {
            "body": "{\"account_id\": \"637423502760\", \"rule_name\": \"sns_topic_without_subscriptions\", \"inspection_date\": \"2024-6-18\", \"report\": {\"message\": \"SNS Topic exists without any subscriptions\", \"remedy\": \"Add subscriptions if required, otherwise delete the topic.\", \"resource_id\": \"arn:aws:sns:eu-west-1:637423502760:lease-locked-dce\", \"region\": \"eu-west-1\", \"account_id\": \"637423502760\"}}"
        },
        {
            "body": "{\"account_id\": \"637423502760\", \"rule_name\": \"sns_topic_without_subscriptions\", \"inspection_date\": \"2024-6-18\", \"report\": {\"message\": \"SNS Topic exists without any subscriptions\", \"remedy\": \"Add subscriptions if required, otherwise delete the topic.\", \"resource_id\": \"arn:aws:sns:eu-west-1:637423502760:account-reset-complete-dce\", \"region\": \"eu-west-1\", \"account_id\": \"637423502760\"}}"
        }
    ]
}

main.handler(event, LambdaContext())
