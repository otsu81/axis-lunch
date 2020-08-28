from abc import ABC, abstractmethod
import logging


class AbstractRestaurant(ABC):

    def __init__(self):
        self.log = logging.getLogger()
        super().__init__()

    @abstractmethod
    def get_week_menu(self, url):
        """
        Fetches the menu of the week from a specific restaurant

        :param str url: the URL of the restaurant page to be scraped
        :return: the week's menu
        :type: dict
        """
        pass

    def make_empty_menu(self, exception):
        self.log.warning(f"Error parsing, {exception}")
        return {
            'mon': 'missing parse',
            'tue': 'missing parse',
            'wed': 'missing parse',
            'thu': 'missing parse',
            'fri': 'missing parse',
        }
