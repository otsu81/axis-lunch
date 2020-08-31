import requests
import logging
import os
from bs4 import BeautifulSoup
from .abstract_restaurant import AbstractRestaurant

logging.basicConfig(level=os.environ.get('LOGLEVEL', 'DEBUG'))
log = logging.getLogger('pieplow_parser')


class Pieplow(AbstractRestaurant):

    def menu_for_weekday(self, menu, weekday):
        weekday_menu = ''
        for line in menu.splitlines():
            if weekday in line:
                weekday_menu += line.replace(f"{weekday}: ", '') + '\n'
        return weekday_menu

    def get_week_menu(self, url):
        try:
            soup = BeautifulSoup(
                requests.get(url).text, 'html.parser'
            )
            week_menu = soup.find_all('div', class_='wpb_wrapper')

            menu_text = ''
            for tag in week_menu[2].find_all('p'):
                menu_text += tag.text + '\n'

            menu = dict()
            menu['mon'] = self.menu_for_weekday(
                menu_text, 'Monday')
            menu['tue'] = self.menu_for_weekday(
                menu_text, 'Tuesday')
            menu['wed'] = self.menu_for_weekday(
                menu_text, 'Wednesday')
            menu['thu'] = self.menu_for_weekday(
                menu_text, 'Thursday')
            menu['fri'] = self.menu_for_weekday(
                menu_text, 'Friday')
            return menu

        except Exception as e:
            return super().make_empty_menu(e)
