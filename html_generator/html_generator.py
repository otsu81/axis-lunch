import os.path
import logging

log = logging.getLogger()


class HTMLGenerator():
    def __init__(
                self, menus: dict,
                index_template_path='',
                menu_template_path='',
                output_path=''
            ):
        if index_template_path == '':
            raise OSError('No index template path is given')
        elif not os.path.exists(index_template_path):
            raise OSError(f"{index_template_path}: file not found")
        else:
            self.index_template_path = index_template_path

        if menu_template_path == '':
            raise OSError('No menu template path is given')
        elif not os.path.exists(menu_template_path):
            raise OSError(f"{menu_template_path}: file not found")
        else:
            self.menu_template_path = menu_template_path

        if output_path == '':
            self.output_path = 'index.html'
        else:
            self.output_path = output_path

        self.menus = menus

    def make_restaurant_rows(self, week_menus):
        with open(self.menu_template_path, 'r') as f:
            menu_template = f.read()

        restaurant_html_rows = str()
        for restaurant in week_menus:
            restaurant_html_rows += menu_template.format(
                restaurant=restaurant, **week_menus[restaurant])

        return restaurant_html_rows

    def make_html(self):
        index = str()
        with open(self.index_template_path, 'r') as f:
            index = f.read()

        restaurant_rows = self.make_restaurant_rows(self.menus)

        index_html = index.format(
            RESTAURANT_MENU_ROWS=restaurant_rows)

        log.warn(f"Generated HTML index: \n{index_html}")

        return index_html
