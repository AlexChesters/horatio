def generate_body(reports):
    items = []

    for report in reports:
        message = report["message"]
        remedy = report["remedy"]
        resource_id = report["resource_id"]

        items.append(f"""
        <h1>{message}</h1>
        <h3>Resource: {resource_id}</h3>
        <p>Remedy: {remedy}</p>
        """)

    return "<br />".join(items)
