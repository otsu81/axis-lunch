import boto3
import logging
import os
from dotenv import load_dotenv
from html_generator import HTMLGenerator

load_dotenv()
log = logging.getLogger()
log.setLevel(level=logging.INFO)


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
    s3.put_object(
        Body=file_contents,
        Bucket=os.environ['S3_BUCKET'],
        Key=object_key,
        ContentType='text/html'
    )


def main(event, context):
    menus = get_restaurant_menu_dict()

    for r in menus:
        for d in menus[r]:
            menus[r][d] = menus[r][d].replace('\n', '</p><p>')

    index_html = HTMLGenerator(
        menus,
        index_template_path=os.environ['INDEX_TEMPLATE_PATH'],
        menu_template_path=os.environ['MENU_TEMPLATE_PATH'],
        output_path=os.environ['OUTPUT_PATH']
    ).make_html()

    copy_html_to_s3(index_html, 'index.html')


if __name__ == '__main__':
    main(None, None)
