import boto3
import logging
import os
from dotenv import load_dotenv
from html_generator import HTMLGenerator

load_dotenv()
log = logging.getLogger()
log.setLevel(level=logging.INFO)


def get_restaurant_menu_dict(ddb_client):
    result = ddb_client.scan(
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


def main(event, context):
    ddb = boto3.client('dynamodb')
    menus = get_restaurant_menu_dict(ddb)

    for r in menus:
        for d in menus[r]:
            menus[r][d] = menus[r][d].replace('\n', '</p><p>')

    grnr = HTMLGenerator(
            menus,
            index_template_path='html_templates/index_template.html',
            menu_template_path='html_templates/row_template.html',
            output_path='html/index.html'
        )

    grnr.make_html()


if __name__ == '__main__':
    main(None, None)
