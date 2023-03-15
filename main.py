
import requests
import datetime as dt

from pprint import pprint
from config import Config

requests_data = {
    'orders' : 'wp-json/wc/v3/orders'
}


def send_request(data: str, after: dt.datetime, before: dt.datetime = dt.datetime.today()) -> requests.models.Response:

    requests_parameters = {
        'after': after.isoformat(),
        'before': before.isoformat()
    }

    response = requests.get(Config.SHOP_URL + requests_data[data],
                    params=requests_parameters,
                    auth=(Config.USER_NAME, Config.API_PASSWORD))
    
    
    return response


response = send_request('orders', dt.datetime.today() - dt.timedelta(days=20))

print(response.json())



