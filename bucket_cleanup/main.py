import boto3
import logging
import requests
import json
import os


log = logging.getLogger('bucket_cleanup')
log.setLevel(os.environ.get('LOGLEVEL', 'INFO'))


class cfnresponse:
    # Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
    # SPDX-License-Identifier: MIT-0
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

    def send(event, context, responseStatus, responseData,
             physicalResourceId=None, noEcho=False):
        responseUrl = event['ResponseURL']

        log.info(f"ResponseUrl: {responseUrl}")

        responseBody = {}
        responseBody['Status'] = responseStatus
        responseBody['Reason'] = 'See the details in CloudWatch Log Stream: ' \
            + context.log_stream_name
        responseBody['PhysicalResourceId'] = physicalResourceId or \
            context.log_stream_name
        responseBody['StackId'] = event['StackId']
        responseBody['RequestId'] = event['RequestId']
        responseBody['LogicalResourceId'] = event['LogicalResourceId']
        responseBody['NoEcho'] = noEcho
        responseBody['Data'] = responseData

        json_responseBody = json.dumps(responseBody)

        log.info("Response body:\n" + json_responseBody)

        headers = {
            'content-type': '',
            'content-length': str(len(json_responseBody))
        }

        try:
            response = requests.put(responseUrl,
                                    data=json_responseBody,
                                    headers=headers)
            log.info("Status code: " + response.reason)
        except Exception as e:
            log.info("send(..) failed executing requests.put(..): " + str(e))


def handler(event, context):
    try:
        bucket = event['ResourceProperties']['BucketName']
        log.info(
            f"bucket: {bucket}, event['RequestType']: {event['RequestType']}"
        )
        if event['RequestType'] == 'Delete':
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(bucket)
            bucket.objects.all().delete()

        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
    except Exception as e:
        log.warning(f"Signaling failure to CloudFormation: {e}")
        cfnresponse.send(event, context, cfnresponse.FAILED, {})
