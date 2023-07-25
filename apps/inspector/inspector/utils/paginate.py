def paginate(fn, result_key, args=None):
    if not args:
        args = {}

    results = []

    fn_result = fn(**args)
    results.append(fn_result[result_key])

    while fn_result.get("NextToken"):
        fn_result = fn(**args, NextToken=fn_result.get("NextToken"))
        results.append(fn_result[result_key])

    return results
