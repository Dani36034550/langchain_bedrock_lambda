# debug without AWS

import json
from lambda_function import lambda_handler

# Simulated Lambda event   ------ Reset query as per your uploaded knowledge document to PineCone
event = {
    # "body": json.dumps({
    #     "query": "What is Amazon Bedrock?"
    # })
    "body": json.dumps({
        "query": "What is Monthly Hosting Cost?"
    })
}

# Call the handler
response = lambda_handler(event, None)
print("Lambda Response:\n", response)
