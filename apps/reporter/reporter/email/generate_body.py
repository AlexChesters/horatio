def generate_body(reports):
    items = []

    if not reports:
        return None

    for item in reports:
        report = item["report"]

        message = report["message"]
        account_id = report["account_id"]
        remedy = report["remedy"]
        resource_id = report["resource_id"]

        items.append(f"""
        <h2>{message} ({account_id})</h2>
        <h3>Resource: {resource_id}</h3>
        <p>Remedy: {remedy}</p>
        """)

    return "<br />".join(items)
