def handler(event, _context):
    print(f"handling event: {event}")

if __name__ == "__main__":
    handler({}, None)
