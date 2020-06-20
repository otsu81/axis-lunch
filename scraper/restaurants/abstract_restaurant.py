from abc import ABC, abstractmethod
import logging


class AbstractRestaurant(ABC):

    def __init__(self):
        self.log = logging.getLogger()
        super().__init__()

    @abstractmethod
    def menu_for_weekday(self, menu_soup, weekday, next_weekday):
        pass

    @abstractmethod
    def get_week_menu(self, url):
        pass

    def make_empty_menu(self, exception):
        self.log.warn(f"Error parsing, {exception}")
        return {
            'mon': 'missing parse',
            'tue': 'missing parse',
            'wed': 'missing parse',
            'thu': 'missing parse',
            'fri': 'missing parse',
        }
