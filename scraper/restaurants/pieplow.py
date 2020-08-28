import requests
import logging
import os
from bs4 import BeautifulSoup
from .abstract_restaurant import AbstractRestaurant

logging.basicConfig(level=os.environ.get('LOGLEVEL', 'DEBUG'))
log = logging.getLogger('pieplow_parser')


class Pieplow(AbstractRestaurant):

    # def menu_for_weekday(self, menu_soup, weekday, next_weekday):
    #     if next_weekday:
    #         next_weekday = menu_soup.index(next_weekday)
    #     return '\n'.join(map(
    #         str, menu_soup[
    #             menu_soup.index(weekday)+1:next_weekday
    #         ]
    #     ))

    def get_week_menu(self, url):
        try:
            soup = BeautifulSoup(
                requests.get(url, verify=False).text, 'html.parser'
            )
            week_menu = soup.find_all('div', class_='wpb_wrapper')

            menu_list = list()
            for tag in week_menu[5].find_all('p'):
                tag.strong.decompose()
                menu_list.append(tag.text)

            print(menu_list)

            weekdays = ['mon', 'tue', 'wed', 'thu', 'fri']
            menu = dict()
            for i, weekday in enumerate(weekdays):
                menu[weekday] = menu_list[i]

            # menu['mon'] = self.menu_for_weekday(
            #     menu_list, 'Monday', 'Tuesday')
            # menu['tue'] = self.menu_for_weekday(
            #     menu_list, 'Tuesday', 'Wednesday')
            # menu['wed'] = self.menu_for_weekday(
            #     menu_list, 'Wednesday', 'Thursday')
            # menu['thu'] = self.menu_for_weekday(
            #     menu_list, 'Thursday', 'Friday')
            # menu['fri'] = self.menu_for_weekday(
            #     menu_list, 'Friday', None)
            return menu

        except Exception as e:
            return super().make_empty_menu(e)
