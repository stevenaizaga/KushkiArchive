import os
import requests
import json
from typing import List, Dict
from urllib.parse import parse_qs

def lambda_handler(event, context):
    # Extract event body
    event_body = event['body']
  
    # Convert event body to a dictionary
    parsed_body = parse_qs(event_body)

    # Alternatively, if you prefer a dictionary with string values instead of lists
    parsed_body = {key: value[0] for key, value in parse_qs(event_body).items()}

    # Prepare the message for Slack
    slack_message = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Estamos trabajando en tu consulta",
            }
        }
    ]

    # Send the message to Slack
    post_message_to_slack("Estamos trabajando en tu consulta", slack_message)
    
    return {
        'statusCode': 200,
        'body': parsed_body
    }

def post_message_to_slack(text: str, blocks: List[Dict[str, str]] = None):
    """Posts a message to a Slack channel."""
    
    slack_token = os.getenv("SLACK_APP_TOKEN")
    slack_channel = os.getenv("SLACK_APP_CHANNEL")

    # Post the message to Slack
    response = requests.post(
        'https://slack.com/api/chat.postMessage', 
        {
            'token': slack_token,
            'channel': slack_channel,
            'text': text,
            'blocks': json.dumps(blocks) if blocks else None
        }
    ).json()

    # Error handling for the Slack API response
    if not response.get("ok"):
        print(f"Error posting message to Slack: {response}")