import boto3
import os
import time
import logging
import json
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
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

    def update_restaurant_menu(self, restaurant_name, menu):
        global to_seconds
        ts = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        update_expression = 'SET #MON = :mon, #TUE = :tue, #WED = :wed, ' \
                            + '#THU = :thu, #FRI = :fri, #TTL = :ttl'

        response = self.client.update_item(
            TableName=self.table_name,
            ExpressionAttributeNames={
                '#MON': 'mon',
                '#TUE': 'tue',
                '#WED': 'wed',
                '#THU': 'thu',
                '#FRI': 'fri',
                '#TTL': 'ttl'
            },
            ExpressionAttributeValues={
                ':mon': {
                    'S': menu['mon']
                },
                ':tue': {
                    'S': menu['tue']
                },
                ':wed': {
                    'S': menu['wed']
                },
                ':thu': {
                    'S': menu['thu']
                },
                ':fri': {
                    'S': menu['fri']
                },
                ':ttl': {
                    'N': str(int(time.time()) + to_seconds['HOUR'])
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
