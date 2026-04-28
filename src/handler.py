import json
import os
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    method = event["httpMethod"]

    if method == "POST" and event.get("path") == "/subscribe":
        body = json.loads(event["body"])
        item = {"PK": body["email"], "SK": "SUBSCRIBER", "name": body.get("name", "")}
        table.put_item(Item=item)
        return response(201, {"message": "subscribed"})

    return response(404, {"message": "not found"})
