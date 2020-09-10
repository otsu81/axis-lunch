import pytest
import csv
from scraper.restaurants import Bricks


@pytest.fixture
def fetch_url():
    restaurants = dict()
    with open('scraper/restaurants.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            restaurants[row[0]] = {'url': row[1]}
    return restaurants['Bricks']['url']


def test_non_missing_parse(fetch_url):
    week_menu = Bricks().get_week_menu(fetch_url)

    assert week_menu['mon'] != 'missing parse'
    assert week_menu['tue'] != 'missing parse'
    assert week_menu['wed'] != 'missing parse'
    assert week_menu['thu'] != 'missing parse'
    assert week_menu['fri'] != 'missing parse'
