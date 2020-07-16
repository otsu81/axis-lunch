from ddb import RestaurantTable
import json


ddb = RestaurantTable()
print(json.dumps(ddb.get_restaurant_menus(), indent=4, default=str))