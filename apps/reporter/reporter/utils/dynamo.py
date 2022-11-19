from boto3.dynamodb.types import TypeDeserializer

def deserialise(input):
    deserialiser = TypeDeserializer()
    result = {}

    for key, value in input.items():
        result[key] = deserialiser.deserialize(value)

    return result

