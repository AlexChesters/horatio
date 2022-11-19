def generate_body(reports):
    print(f"reports: {reports}")
    items = []

    for item in reports:
        report = item["report"]

        message = report["message"]
        account_id = report["account_id"]
        remedy = report["remedy"]
        resource_id = report["resource_id"]

        items.append(f"""
        <h1>{message} ({account_id})</h1>
        <h3>Resource: {resource_id}</h3>
        <p>Remedy: {remedy}</p>
        """)

    return "<br />".join(items)
