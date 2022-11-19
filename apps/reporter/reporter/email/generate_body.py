def generate_body(reports):
    print(f"reports: {reports}")

    items = []

    for report in reports:
        print(f"report: {report}")
        message = report["message"]
        remedy = report["remedy"]
        resource_id = report["resource_id"]

        items.append(f"""
        <h1>{message}</h1>
        <h3>Resource: {resource_id}</h3>
        <p>Remedy: {remedy}</p>
        """)

    return "<br />".join(items)
