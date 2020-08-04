import os
import json
import logging
from restaurants.paolos import Paolos
from restaurants.pieplow import Pieplow
from ddb import RestaurantTable

logging.basicConfig(level=os.environ.get('LOGLEVEL'))
log = logging.getLogger('scraper')


def handler(event, context):
    paolos_menu = Paolos().get_week_menu(os.environ['PAOLOS'])
    pieplow_menu = Pieplow().get_week_menu(os.environ['PIEPLOW'])

    menu = {
        'Paolos': paolos_menu,
        'Pieplow': pieplow_menu
    }

    ddb = RestaurantTable()
    for r in menu:
        ddb.update_restaurant_menu(
            r, menu[r]
        )

    log.info(json.dumps(menu, indent=4, default=str))
    return json.dumps(
        {'success': 'true'}
    )


if __name__ == '__main__':
    handler(None, None)
