import requests
import logging
import os
from .abstract_restaurant import AbstractRestaurant
from bs4 import BeautifulSoup

logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))
log = logging.getLogger('bricks_parser')


class Bricks(AbstractRestaurant):

    def __make_weekday_menu(self, soup):
        weekday_menu = str()
        for i in range(len(soup)):
            if i % 3 == 1:
                menu_item = soup[i].text
                weekday_menu += menu_item[:menu_item.find('\n')] + '\n'
        return weekday_menu

    def get_week_menu(self, url):
        try:
            soup = BeautifulSoup(
                requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text,
                'html.parser'
            )
            menu_soup = soup.find('div', class_='lunch')
            menu_items = menu_soup.find_all('table')

            weekdays = ['mon', 'tue', 'wed', 'thu', 'fri']
            menu = dict()
            for index, weekday in enumerate(weekdays):
                day_menu_soup = menu_items[index].find_all('td')
                menu[weekday] = self.__make_weekday_menu(day_menu_soup)
            return menu

        except Exception as e:
            return super().make_empty_menu(e)
