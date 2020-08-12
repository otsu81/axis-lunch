import boto3
import logging
import json
import os
from boto3.dynamodb.conditions import Key
from html_generator import HTMLGenerator

logging.basicConfig(level=os.environ.get('LOGLEVEL'))
log = logging.getLogger('html_generator')


def get_restaurant_menus_dict(restaurants):

    print(restaurants)

    ddb = boto3.resource('dynamodb')
    table = ddb.Table(os.environ.get('TABLE_NAME'))

    menus = dict()
    for r in restaurants:
        result = table.query(
            IndexName='sortByDate',
            ConsistentRead=False,
            ScanIndexForward=False,
            Limit=1,
            KeyConditionExpression=Key('restaurant').eq(r)
        )
        result['Items'][0].pop('restaurant')
        result['Items'][0].pop('fetchDate')
        menus[r] = result['Items'][0]

    log.info(json.dumps(menus, indent=4, default=str))
    return menus


def copy_html_to_s3(file_contents, object_key):
    s3 = boto3.client('s3')
    result = s3.put_object(
        Body=file_contents,
        Bucket=os.environ['S3_BUCKET'],
        Key=object_key,
        ContentType='text/html'
    )
    log.info(json.dumps(result, indent=4, default=str))


def main(event, context):
    menus = get_restaurant_menus_dict(event['restaurants'])

    for r in menus:
        for d in menus[r]:
            menus[r][d] = menus[r][d].replace('\n', '</p><p>')
            log.debug(menus[r][d])

    index_html = HTMLGenerator(
        menus,
        index_template_path=os.environ['INDEX_TEMPLATE_PATH'],
        menu_template_path=os.environ['MENU_TEMPLATE_PATH'],
        output_path=os.environ['OUTPUT_PATH']
    ).make_html()

    copy_html_to_s3(index_html, 'index.html')


def handler(event, context):
    log.info(json.dumps(event, indent=4, default=str))
    main(event, context)
