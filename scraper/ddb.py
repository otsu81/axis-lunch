import boto3
import os
import time
import logging
import json
from datetime import datetime


to_seconds = {
    'HOUR': 3600,
    'DAY': 86400,
    'WEEK': 604800
}
logging.basicConfig(level=os.environ.get('LOGLEVEL'))
log = logging.getLogger('ddb_table')


class RestaurantTable():

    def __init__(self):
        self.client = boto3.client('dynamodb')
        self.table_name = os.environ.get('TABLE_NAME')

    def update_restaurant_item(self, restaurant_name, restaurant_info):
        global to_seconds
        ts = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')

        update_expression = 'SET #MON = :mon, #TUE = :tue, #WED = :wed, ' \
                            + '#THU = :thu, #FRI = :fri, #TTL = :ttl, ' \
                            + '#URL = :url'

        response = self.client.update_item(
            TableName=self.table_name,
            ExpressionAttributeNames={
                '#MON': 'mon',
                '#TUE': 'tue',
                '#WED': 'wed',
                '#THU': 'thu',
                '#FRI': 'fri',
                '#TTL': 'ttl',
                '#URL': 'url'
            },
            ExpressionAttributeValues={
                ':mon': {
                    'S': restaurant_info['mon']
                },
                ':tue': {
                    'S': restaurant_info['tue']
                },
                ':wed': {
                    'S': restaurant_info['wed']
                },
                ':thu': {
                    'S': restaurant_info['thu']
                },
                ':fri': {
                    'S': restaurant_info['fri']
                },
                ':url': {
                    'S': restaurant_info['url']
                },
                ':ttl': {
                    'N': str(int(time.time()) + to_seconds['DAY'])
                }
            },
            Key={
                'restaurant': {
                    'S': restaurant_name
                },
                'fetchDate': {
                    'S': ts
                },
            },
            UpdateExpression=update_expression
        )
        log.info(json.dumps(response, indent=4, default=str))

    def get_restaurant_items(self):
        log.info('SCAN operation: Getting all menu items')
        return self.client.scan(
            TableName=self.table_name,
            IndexName='restaurant-index'
        )
