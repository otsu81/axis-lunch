import requests
from bs4 import BeautifulSoup
from restaurants.abstract_restaurant import AbstractRestaurant


class Pieplow(AbstractRestaurant):

    def menu_for_weekday(self, menu_soup, weekday, next_weekday):
        if next_weekday:
            next_weekday = menu_soup.index(next_weekday)
        return '\n'.join(map(
            str, menu_soup[
                menu_soup.index(weekday)+1:next_weekday
            ]
        ))

    def get_week_menu(self, url):
        try:
            soup = BeautifulSoup(requests.get(url).text, 'html.parser')
            week_menu = soup.find_all('div', class_='wpb_wrapper')

            menu_list = list()
            for tag in week_menu[6].find_all('p'):
                for child in tag.children:
                    menu_list.append(child.string.rstrip())

            print(menu_list)

            menu = dict()
            menu['mon'] = self.menu_for_weekday(
                menu_list, 'Monday', 'Tuesday')
            menu['tue'] = self.menu_for_weekday(
                menu_list, 'Tuesday', 'Wednesday')
            menu['wed'] = self.menu_for_weekday(
                menu_list, 'Wednesday', 'Thursday')
            menu['thu'] = self.menu_for_weekday(
                menu_list, 'Thursday', 'Friday')
            menu['fri'] = self.menu_for_weekday(
                menu_list, 'Friday', None)

            return menu
        except Exception as e:
            return super().make_empty_menu(e)
