import requests
import logging
import pprint
import os
from bs4 import BeautifulSoup
from restaurants.abstract_restaurant import AbstractRestaurant

logging.basicConfig(level=os.environ.get('LOGLEVEL'))
log = logging.getLogger('paolos_parser')


class Paolos(AbstractRestaurant):

    # def menu_for_weekday(self, menu_soup, weekday, next_weekday):
    #     return '\n'.join(
    #         map(str,
    #             menu_soup[
    #                 menu_soup.index(weekday)+1:menu_soup.index(next_weekday)-1
    #                 ]
    #             )
    #         ).rstrip()

    def get_week_menu(self, url):
        try:
            soup = BeautifulSoup(requests.get(url).text, 'html.parser')
            menu_head = soup.find_all('div', {'class': 'menu-block__desc'})

            weekdays = ['mon', 'tue', 'wed', 'thu', 'fri']
            menu = dict()
            for weekday, result in enumerate(weekdays):
                weekday_menu = list()
                for tag in menu_head[weekday]:
                    if tag.string:
                        stripped = tag.string.lstrip().rstrip()
                        if stripped != '':
                            weekday_menu.append(stripped)
                menu[result] = ', '.join(weekday_menu)

            return menu

        except Exception as e:
            return super().make_empty_menu(e)
