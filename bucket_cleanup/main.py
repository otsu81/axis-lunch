import boto3
import logging
import cfnresponse
import os


log = logging.getLogger('bucket_cleanup')
log.setLevel(os.environ.get('LOGLEVEL', 'WARNING'))


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