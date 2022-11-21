from aws_lambda_powertools import Logger

from reporter.db.dynamo import get_todays_reports
from reporter.email.generate_body import generate_body
from reporter.email.send_email import send_email

logger = Logger()

@logger.inject_lambda_context(log_event=True)
def handler(_event, _context):
    reports = get_todays_reports()
    body = generate_body(reports)
    send_email(body)

if __name__ == "__main__":
    handler({}, None)
