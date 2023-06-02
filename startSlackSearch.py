import boto3
import json

def lambda_handler(event, context):
    client = boto3.client('stepfunctions')

    response = client.start_execution(
        stateMachineArn='arn:aws:states:us-east-1:568808263449:stateMachine:slackBot',
        input=json.dumps(event)
    )

    return {
        'statusCode': 200
    }