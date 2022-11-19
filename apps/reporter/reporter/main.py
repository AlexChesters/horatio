from reporter.db.dynamo import get_todays_data

def handler(event, _context):
    print(f"handling event: {event}")

    results = get_todays_data()

    for result in results:
        print(f"result: {result}")

if __name__ == "__main__":
    handler({}, None)
