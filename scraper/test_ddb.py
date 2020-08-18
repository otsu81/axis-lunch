import json
from restaurants.pieplow import Pieplow


p = Pieplow()
print(
    json.dumps(
        p.get_week_menu("https://lund.pieplowsmat.se/street-food/")
    )
)