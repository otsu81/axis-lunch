# import requests
# import urllib.request
# import time
import os
import json
import logging
from dotenv import load_dotenv
from restaurants.paolos import Paolos
from restaurants.pieplow import Pieplow
from ddb import RestaurantTable

load_dotenv()
log = logging.getLogger()


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
