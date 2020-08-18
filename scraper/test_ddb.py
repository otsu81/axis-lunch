import json
from restaurants.paolos import Paolos


p = Paolos()
print(
    json.dumps(
        p.get_week_menu("https://www.paolositalian.se/menyer/lund/")
    )
)