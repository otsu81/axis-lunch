import requests
import logging
import os
import json
import time
from datetime import datetime
from .abstract_restaurant import AbstractRestaurant

logging.basicConfig(level=os.environ.get('LOGLEVEL', 'DEBUG'))
log = logging.getLogger('scotland_parser')


class ScotlandYard(AbstractRestaurant):

    def get_week_menu(self, url):
        try:
            # easier to use API directly and get JSON response,
            # append URL with header
            today = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
            header = 'week?language=sv&restaurantPageId=188211&weekDate=' \
                + today
            url = url + header
            logging.debug(url)

            response = requests.get(url)
            json_data = json.loads(response.text)

            menu = dict()
            for day_json in json_data['LunchMenus']:
                if day_json.get('Html'):
                    day_html = day_json['Html']

                if day_json.get('DayOfWeek') == 'Måndag':
                    menu['mon'] = day_html
                elif day_json.get('DayOfWeek') == 'Tisdag':
                    menu['tue'] = day_html
                elif day_json.get('DayOfWeek') == 'Onsdag':
                    menu['wed'] = day_html
                elif day_json.get('DayOfWeek') == 'Torsdag':
                    menu['thu'] = day_html
                elif day_json.get('DayOfWeek') == 'Fredag':
                    menu['fri'] = day_html
            return menu

        except Exception as e:
            return super().make_empty_menu(e)
