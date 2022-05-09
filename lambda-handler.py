"""Basic function to simulate an import of an external library
and a call to it.
"""
import requests
import json


def lambda_handler(event, context):
    """Handler to clear all records from redis.
    """
    print(f"Lambda handler called, calling reuqests now.")

    r = requests.get('https://www.google.com')

    print(r)
    print(r.content)

    return {
        'statusCode': 200,
        'body': json.dumps(str(r.content))
    }
