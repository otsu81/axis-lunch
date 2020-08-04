import boto3
import logging
import json
import os
from html_generator import HTMLGenerator

logging.basicConfig(level=os.environ.get('LOGLEVEL'))
log = logging.getLogger('html_generator')


def get_restaurant_menu_dict():
    ddb = boto3.client('dynamodb')
    result = ddb.scan(
        TableName=os.environ.get('TABLE_NAME'),
        IndexName=os.environ.get('TABLE_GSI')
    )
    restaurant_menus = dict()
    for r in result['Items']:
        restaurant_menus[r['restaurant']['S']] = {
            'mon': r['mon']['S'],
            'tue': r['tue']['S'],
            'wed': r['wed']['S'],
            'thu': r['thu']['S'],
            'fri': r['fri']['S']
        }
    return restaurant_menus


def copy_html_to_s3(file_contents, object_key):
    s3 = boto3.client('s3')
    result = s3.put_object(
        Body=file_contents,
        Bucket=os.environ['S3_BUCKET'],
        Key=object_key,
        ContentType='text/html'
    )
    log.info(json.dumps(result, indent=4, default=str))


def main():
    menus = get_restaurant_menu_dict()

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
    main()