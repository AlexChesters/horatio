import unittest

from reporter.utils.dynamo import deserialise

class DynamoDBUtilsTests(unittest.TestCase):

    def test_deserialise(self):
        input = {
            "number_key": {
                "N": 1241413,
            },
            "string_key": {
                "S": "foo"
            },
            "map_key": {
                "M": {
                    "bar": {
                        "S": "buzz"
                    }
                }
            }
        }

        expected = {
            "number_key": 1241413,
            "string_key": "foo",
            "map_key": {
                "bar": "buzz"
            }
        }

        self.assertEqual(deserialise(input), expected, "Deserialise should convert DynamoDB JSON to normal JSON")
