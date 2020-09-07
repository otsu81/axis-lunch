import os
import json
import logging
import csv
from restaurants import Paolos
from restaurants import Pieplow
from restaurants import Edison
from restaurants import Bricks
from ddb import RestaurantTable

logging.basicConfig(level=os.environ.get('LOGLEVEL', 'WARNING'))
log = logging.getLogger('scraper')


def handler(event, context):

    # define all restaurants to be parsed and generated
    classmap = {
        'Paolos': Paolos(),
        'Edison': Edison(),
        'Pieplow Grenden': Pieplow()
        'Bricks': Bricks()
    }

    # get URLs for respective restaurants
    restaurants = dict()
    with open('restaurants.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            restaurants[row[0]] = classmap[row[0]].get_week_menu(row[1])
            restaurants[row[0]]['url'] = row[1]

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
