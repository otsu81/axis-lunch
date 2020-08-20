from scraper.restaurants.paolos import Paolos


def test_non_missing_parse():
    paolos_url = 'https://www.paolositalian.se/menyer/lund/'

    week_menu = Paolos().get_week_menu(paolos_url)

    assert week_menu['mon'] != 'missing parse'


test_non_missing_parse()
