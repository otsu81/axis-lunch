import requests
from bs4 import BeautifulSoup
from restaurants.abstract_restaurant import AbstractRestaurant

logging.basicConfig(level=os.environ.get('LOGLEVEL'))
log = logging.getLogger('paolos_parser')

class Paolos(AbstractRestaurant):

    def menu_for_weekday(self, menu_soup, weekday, next_weekday):
        return '\n'.join(map(
            str, menu_soup[
                menu_soup.index(weekday)+1:menu_soup.index(next_weekday)-1
            ]
        ))

    def get_week_menu(self, url):
        try:
            soup = BeautifulSoup(requests.get(url).text, 'html.parser')
            hotel_head = soup.find('div', {'class': 'hotelhead'})

            menu_list = list()
            for tag in hotel_head.find_all('p'):
                for child in tag.children:
                    if child.string and ',' not in child.string:
                        menu_list.append(child.string.rstrip())

            menu = dict()
            menu['mon'] = self.menu_for_weekday(menu_list, 'MÅNDAG', 'TISDAG')
            menu['tue'] = self.menu_for_weekday(menu_list, 'TISDAG', 'ONSDAG')
            menu['wed'] = self.menu_for_weekday(menu_list, 'ONSDAG', 'TORSDAG')
            menu['thu'] = self.menu_for_weekday(menu_list, 'TORSDAG', 'FREDAG')
            menu['fri'] = self.menu_for_weekday(
                menu_list, 'FREDAG', 'PÅ KVÄLLEN')

            return menu
        except Exception as e:
            return super().make_empty_menu(e)
