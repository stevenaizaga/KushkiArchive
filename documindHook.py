import os
import requests
import json
from typing import List, Dict

def lambda_handler(event, context):
    """Main function that handles an event and context, and sends data to Slack."""
    
    body = event["body"]
    text = body["text"]
    
    # Retrieve Documind response
    documind_response = get_documind_response(text)
    
    # Parse Documind response
    parsed_data = parse_documind_response(documind_response)

    # Construct Slack message
    slack_message = build_slack_message(text, parsed_data)

    # Post the message to Slack
    post_message_to_slack("Tengo la data", slack_message)

    return {"statusCode": 200, "body": json.dumps("aaah")}

def get_documind_response(query: str):
    """Send a query to Documind and return the response."""
    
    payload = json.dumps({"question": query +" en español", "index": 2})
    headers = {
        "authority": "documind.onrender.com",
        "authorization": "Bearer: " + os.getenv("DOCUMIND_TOKEN"),
        "content-type": "application/json",
    }
    
    response = requests.post(
        "https://documind.onrender.com/ask-from-collection-stream",
        data=payload,
        headers=headers,
        stream=True,
    )
    
    response_content = [line for line in response.iter_lines(decode_unicode=False) if line]
    return response_content[-1]

def parse_documind_response(response: bytes):
    """Parse the response from Documind into a more usable format."""
    
    decoded_response = response.decode()[5:]
    parsed_response = json.loads(decoded_response)
    data = parsed_response["data"]
    
    return {
        "answer": data["answer"],
        "documents": data["documents"],
        "url_file": data["documents"][0]["file_url"],
    }

def build_slack_message(text: str, data: Dict[str, str]):
    
    return [
        {"type": "header", "text": {"type": "plain_text", "text": text}},
        {"type": "section", "text": {"type": "mrkdwn", "text": data["answer"]}},
        {
            "type": "actions",
            "block_id": "actionblock789",
            "elements": [{"type": "button", "text": {"type": "plain_text", "text": "Documentación en pdf"}, "url": data["url_file"]}],
        },
    ]

def post_message_to_slack(text: str, blocks: List[Dict[str, str]] = None):
    """Post a message to a Slack channel."""
    
    slack_token = os.getenv("SLACK_APP_TOKEN")
    slack_channel = os.getenv("SLACK_APP_CHANNEL")
    
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        {
            "token": slack_token,
            "channel": slack_channel,
            "text": text,
            "blocks": json.dumps(blocks) if blocks else None,
        },
    ).json()
    
    # Error handling for the Slack API response
    if not response.get("ok"):
        print(f"Error posting message to Slack: {response}")
