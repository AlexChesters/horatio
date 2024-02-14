from dataclasses import dataclass

from inspector import main

@dataclass
class LambdaContext:
    function_name: str = "test"
    memory_limit_in_mb: int = 128
    invoked_function_arn: str = "arn:aws:lambda:eu-west-1:809313241:function:test"
    aws_request_id: str = "52fdfc07-2182-154f-163f-5f0f9a621d72"

event = {
    "SERVICE": "CODEPIPELINE",
    "REGIONS": ["eu-west-1"]
}

main.handler(event, LambdaContext())
