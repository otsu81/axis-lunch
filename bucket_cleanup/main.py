import json
import boto3
import logging
import os
from botocore.vendored import requests


log = logging.getLogger('bucket_cleanup')
log.setLevel(os.environ.get('LOGLEVEL', 'WARNING'))


def handler(event, context):
    try:
        bucket = event['ResourceProperties']['BucketName']

        if event['RequestType'] == 'Delete':
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(bucket)
            for obj in bucket.objects.filter():
                s3.Object(bucket.name, obj.key).delete()

        sendResponseCfn(event, context, "SUCCESS")
    except Exception as e:
        log.warning(e)
        sendResponseCfn(event, context, "FAILED")


def sendResponseCfn(event, context, responseStatus):
    response_body = {
        'Status': responseStatus,
        'Reason': 'Log stream name: ' + context.log_stream_name,
        'PhysicalResourceId': context.log_stream_name,
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'Data': json.loads("{}")
    }

    requests.put(event['ResponseURL'], data=json.dumps(response_body))
    return response_body
