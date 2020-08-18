import requests
import logging
import os
from bs4 import BeautifulSoup
from restaurants.abstract_restaurant import AbstractRestaurant

logging.basicConfig(level=os.environ.get('LOGLEVEL'))
log = logging.getLogger('paolos_parser')


class Paolos(AbstractRestaurant):

    def menu_for_weekday(self, menu_list, weekday, next_weekday):
        return '\n'.join(
            map(str,
                menu_list[
                    menu_list.index(weekday)+1:menu_list.index(next_weekday)
                    ]
                )
            )

    def get_week_menu(self, url):
        try:
            soup = BeautifulSoup(requests.get(url).text, 'html.parser')

            menu_head = soup.find_all('div', {'class': 'menu-block__text'})
            items = menu_head[0].find_all(['p', 'h4'])

            for i in items:
                spans = i.find_all('span', {'class': 'menu-block__price'})
                if spans:
                    spans[0].extract()

            menu_list = list()
            for i in items:
                item = i.get_text().lstrip().rstrip()
                if item != '':
                    menu_list.append(item)

            menu = dict()
            menu['mon'] = self.menu_for_weekday(menu_list, 'Måndag', 'Tisdag')
            menu['tue'] = self.menu_for_weekday(menu_list, 'Tisdag', 'Onsdag')
            menu['wed'] = self.menu_for_weekday(menu_list, 'Onsdag', 'Torsdag')
            menu['thu'] = self.menu_for_weekday(menu_list, 'Torsdag', 'Fredag')
            menu['fri'] = self.menu_for_weekday(menu_list, 'Fredag', 'Lördag')

            return menu

        except Exception as e:
            log.warn(f"Exception parsing Paolos, {e}")
            return super().make_empty_menu(e)
