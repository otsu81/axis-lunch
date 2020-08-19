import json
from ..scraper.restaurants.paolos import Paolos


p = Paolos()
print(
    json.dumps(
        p.get_week_menu("https://www.paolositalian.se/menyer/lund/"),
        indent=4, default=str
    )
)