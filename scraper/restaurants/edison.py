import requests
import logging
import os
from bs4 import BeautifulSoup
from .abstract_restaurant import AbstractRestaurant

logging.basicConfig(level=os.environ.get('LOGLEVEL', 'WARNING'))
log = logging.getLogger('edison_parser')


class Edison(AbstractRestaurant):

    def menu_for_weekday(self, menu_soup, weekday, next_weekday):
        soup = menu_soup.find(
            'div', {'id': weekday}).find_all(
                'td', {'class': 'course_description'})

        menu = str()
        for course in soup:
            for p in course.find_all('p'):
                for child in p.children:
                    if child.string.rstrip():
                        menu += f"{child.string.rstrip()}\n"
        return menu

    def get_week_menu(self, url):
        try:
            soup = BeautifulSoup(requests.get(url).text, 'html.parser')
            menu = dict()
            menu['mon'] = self.menu_for_weekday(soup, 'monday', None)
            menu['tue'] = self.menu_for_weekday(soup, 'tuesday', None)
            menu['wed'] = self.menu_for_weekday(soup, 'wednesday', None)
            menu['thu'] = self.menu_for_weekday(soup, 'thursday', None)
            menu['fri'] = self.menu_for_weekday(soup, 'friday', None)

            return menu

        except Exception as e:
            return super().make_empty_menu(e)
