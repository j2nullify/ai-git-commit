"""Query Ollama model
"""

import json
import boto3

# Initialize the Bedrock client
# bedrock_client = boto3.client('bedrock', region_name="us-east-1")
bedrock_runtime = boto3.client('bedrock-runtime', region_name="us-east-1")

def query_bedrock(prompt: str, stream: bool = True):
    model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    
    # Prepare the payload
    anthropic_version: str = "bedrock-2023-05-31"

    body = {
        "anthropic_version": anthropic_version,
        "max_tokens": 1000,
        "system": "You are a software developer from Stripe writing git commits for other companies.",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
    }

    # Make the request to the Bedrock API
    # Invoke the model with the request
    streaming_response = bedrock_runtime.invoke_model_with_response_stream(
        modelId=model_id,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )
    
    # Process the response
    full_response = ""
    if stream:
        print("streaming...")
        # Extract and print the response text in real-time
        for event in streaming_response["body"]:
            chunk = json.loads(event["chunk"]["bytes"])
            if "delta" in chunk:
                if "text" in chunk["delta"]:
                    text = chunk["delta"]["text"]
                    print(text, end="")
                    full_response += text
        print()  # Print a newline at the end
    else:
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )
        full_response = json.loads(response['body'].read())['completion']
        print(full_response)
    
    return full_response.strip()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        query_bedrock(prompt)
    else:
        print("Please provide a prompt as a command-line argument.")

