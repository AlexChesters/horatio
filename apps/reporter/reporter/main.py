from reporter.db.dynamo import get_todays_reports
from reporter.email.generate_body import generate_body

def handler(event, _context):
    print(f"handling event: {event}")

    reports = get_todays_reports()
    body = generate_body(reports)

    print(f"body: {body}")

if __name__ == "__main__":
    handler({}, None)
