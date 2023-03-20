
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


response = get_orders(after=dt.datetime.today() - dt.timedelta(days=79))

df = pd.DataFrame(response, columns=['id', 'total', 'status', 'line_items', 'customer_id',  'date_completed'])
df['total'] =  pd.to_numeric(df['total'])

#
df = df.set_index(['id'])

## filter only completed
df = df.loc[df['status'] == 'completed']

new_df = pd.DataFrame()

for pos in df.iterrows():
    row = pos[1]
    
    for line in pos[1]['line_items']:
        
        new_series = pd.DataFrame({'cena': line['price'],
                                'status': row['status'],
                                'użytkownik': row['customer_id'],
                                'data':row['date_completed'],
                                'produkt': line['parent_name'] if line['parent_name'] is not None else line['name'],
                                'wariant': line['meta_data'][0].get('value') if line['meta_data'] != [] else None
                                }, index=[line['id']])

        new_df = pd.concat([new_df, new_series], axis=0)

 
new_df['cena'] =  pd.to_numeric(new_df['cena'])
print(new_df)
print(len(new_df))
print(new_df.sum(numeric_only=True))