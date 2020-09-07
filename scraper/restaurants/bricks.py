import requests
import logging
import os
import requests
from .abstract_restaurant import AbstractRestaurant
from bs4 import BeautifulSoup, Tag, NavigableString

logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))
log = logging.getLogger('bricks_parser')


class Bricks(AbstractRestaurant):

    def __make_weekday_menu(self, soup):
        weekday_menu = str()
        for i in range(len(soup)):
            if i%3 == 1:
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

                # menu_item = td[1].text
                # menu_item = menu_item[:menu_item.find('\n')]
                # print(menu_item)
                # if isinstance(child, Tag):
                #     td = child.find_all('td')
                #     menu_item = td[1].text
                #     menu_item = menu_item[:menu_item.find('\n')]
                #     print(menu_item)




            # pass1 = [tag.text for tag in week_menu.find_all('td')]
            # pass2 = list()
            # for i in range(len(pass1)):
            #     if i%3 == 1:
            #         substr = pass1[i][:pass1[i].find('\r')]
            #         pass2.append(substr)

            # for i in range(len(pass2)):
            #     print(f"{i}: {pass2[i]}")


        except Exception as e:
            return super().make_empty_menu(e)

