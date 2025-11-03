import json
from chain_builder import build_chain

def lambda_handler(event, context):
    try:
        # Parse request body
        body = json.loads(event.get("body", "{}"))

        # ✅ Require user-provided query
        query = body.get("query")
        if not query:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required field: 'query'"})
            }

        chain = build_chain()
        result = chain.invoke({"query": query})

        # Extract result
        answer = result.get("result", str(result)) if isinstance(result, dict) else str(result)

        return {
            "statusCode": 200,
            "body": json.dumps({"answer": answer})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
