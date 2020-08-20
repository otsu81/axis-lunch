import os
import json
import logging
from csv import DictReader
from restaurants.paolos import Paolos
from restaurants.pieplow import Pieplow
from restaurants.edison import Edison
from ddb import RestaurantTable

logging.basicConfig(level=os.environ.get('LOGLEVEL', 'WARNING'))
log = logging.getLogger('scraper')


def handler(event, context):

    # define all restaurants to be parsed and generated
    classmap = {
        'Paolos': Paolos(),
        'Edison': Edison(),
        'Pieplow': Pieplow()
    }

    # get URLs for respective restaurants
    restaurants = dict()
    with open('restaurants_sandbox.csv', 'r') as f:
        reader = DictReader(f)
        for row in reader:
            restaurants[row['restaurant']]['url'] = row['url']
            restaurants[row['restaurant']] = \
                classmap[row['restaurant']].get_week_menu(row['url'])

    # update the DDB table with restaurant menus
    ddb = RestaurantTable(table_name=os.environ.get('TABLE_NAME'))
    for r in restaurants:
        ddb.update_restaurant_item(
            r, restaurants[r]
        )

    log.info(json.dumps(restaurants, indent=4, default=str))

    # return list of attempted restaurants
    return {
            'success': 'true',
            'restaurants': list(restaurants.keys())
        }


if __name__ == '__main__':
    handler(None, None)
