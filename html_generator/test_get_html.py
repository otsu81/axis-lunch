import requests
import os
# import urllib.request
from dotenv import load_dotenv

load_dotenv()


def write_html(restaurant_name):
    with open(f"html/{restaurant_name}.html", 'w') as f:
        f.write(
            requests.get(os.environ[restaurant_name]).text
        )


write_html('PAOLOS')
write_html('PIEPLOW')