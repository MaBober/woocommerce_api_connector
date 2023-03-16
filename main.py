
import requests
import datetime as dt
import pandas as pd

from pprint import pprint
from config import Config

requests_data = {
    'orders' : 'wp-json/wc/v3/orders'
}


def get_orders(after: dt.datetime, before: dt.datetime = dt.datetime.today()) -> requests.models.Response:
    
    page_nr = 1
    total_response = []

    while True:

        requests_parameters = {
            'after': after.isoformat(),
            'before': before.isoformat(),
            'per_page': 20,
            'page': page_nr
        }

        page_response = requests.get(Config.SHOP_URL + requests_data['orders'],
                        params=requests_parameters,
                        auth=(Config.USER_NAME, Config.API_PASSWORD))

        if len(page_response.json()) == 0:
            break

        total_response.extend(page_response.json())
        page_nr +=1
 
    return total_response




response = get_orders(after=dt.datetime.today() - dt.timedelta(days=40))

pprint(len(response))




