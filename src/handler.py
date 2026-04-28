import json
import os
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)


def response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps(body, cls=DecimalEncoder),
    }


def lambda_handler(event, context):
    method = event["httpMethod"]
    path = event.get("path", "")

    if method == "GET" and path == "/items":
        result = table.scan()
        return response(200, result.get("Items", []))

    if method == "POST" and path == "/items":
        body = json.loads(event["body"])
        table.put_item(Item=body)
        return response(201, body)

    if method == "DELETE" and path.startswith("/items/"):
        pk = path.split("/")[-1]
        table.delete_item(Key={"PK": pk, "SK": pk})
        return response(200, {"deleted": pk})

    return response(404, {"message": "not found"})
