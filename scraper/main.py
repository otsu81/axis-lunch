import os
import json
import logging
from restaurants.paolos import Paolos
from restaurants.pieplow import Pieplow
from restaurants.edison import Edison
from ddb import RestaurantTable

logging.basicConfig(level=os.environ.get('LOGLEVEL'))
log = logging.getLogger('scraper')


def handler(event, context):

    classmap = {
        'Paolos': Paolos(),
        'Edison': Edison(),
        'Pieplow': Pieplow()
    }

    restaurants = dict()
    with open('restaurants.csv', 'r') as f:
        for r in f.readlines():
            info = r.rstrip().split(',')
            restaurants[info[0]] = info[1]
            restaurants[info[0]]['menu'] = \
                classmap[info[0]].get_week_menu(info[1])

    ddb = RestaurantTable()
    for r in restaurants:
        ddb.update_restaurant_menu(
            r, r['menu']
        )

    log.info(json.dumps(restaurants, indent=4, default=str))

    return json.dumps(
        {
            'success': 'true',
            'restaurants': restaurants.keys()
        }
    )


if __name__ == '__main__':
    handler(None, None)
