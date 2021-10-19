import json
import os
import boto3

# import requests


def get_count_handler(event, context):
    """Visitor counter Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    table_name = os.environ.get('DB_NAME', 'crc-aws-db')
    key_name = os.environ.get('DB_KEY', 'visitors')

    try:
        # TODO: Error if the table doesn't exist
        client = boto3.client('dynamodb')
        response = client.get_item(
            TableName=table_name,
            Key={
                'name': {'S': key_name}
            }
        )

        item = response['Item']
        count = int(item['visitors']['N'])
    except:
        count = 0

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "message": "success",
            "count": count
        }),
    }

def add_count_handler(event, context):
    """Visitor counter Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    table_name = os.environ.get('DB_NAME', 'crc-aws-db')
    key_name = os.environ.get('DB_KEY', 'visitors')

    client = boto3.client('dynamodb')
    response = client.update_item(
        TableName=table_name,
        Key={'name': {
            'S': key_name
            }
        },
        ExpressionAttributeValues={
            ':inc': {'N': '1'}
        },
        UpdateExpression="ADD visitors :inc"
    )

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "message": "success"
        }),
    }