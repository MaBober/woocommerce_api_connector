import requests
import datetime as dt
import pandas as pd


class WooShop:

    requests_data = {
    'orders' : 'wp-json/wc/v3/orders'
    }


    def __init__(self, shop_url, user, password) -> None:

        self.url = shop_url
        self.user = user
        self.passowrd = password


    def get_raw_orders(self, after: dt.datetime, before: dt.datetime = dt.datetime.today()) -> requests.models.Response:
    
        page_nr = 1
        total_response = []

        while True:

            requests_parameters = {
                'after': after.isoformat(),
                'before': before.isoformat(),
                'per_page': 20,
                'page': page_nr
            }

            page_response = requests.get(self.url + WooShop.requests_data['orders'],
                            params=requests_parameters,
                            auth=(self.user, self.passowrd))

            if len(page_response.json()) == 0:
                break

            total_response.extend(page_response.json())
            page_nr +=1
    
        return total_response
    
    def get_basic_orders_data(self, after: dt.datetime, before: dt.datetime = dt.datetime.today(), only_completed=True) -> pd.DataFrame :

        response = self.get_raw_orders(after=after, before=before)

        raw_data = pd.DataFrame(response, columns=['id', 'total', 'status', 'line_items', 'customer_id',  'date_completed'])
        raw_data['total'] =  pd.to_numeric(raw_data['total'])

        raw_data = raw_data.set_index(['id'])

        if only_completed is True:
            raw_data = raw_data.loc[raw_data['status'] == 'completed']

        basic_orders_data = pd.DataFrame()

        for pos in raw_data.iterrows():
            row = pos[1]
            
            for line in pos[1]['line_items']:
                
                new_series = pd.DataFrame({'cena': line['price'],
                                        'status': row['status'],
                                        'użytkownik': row['customer_id'],
                                        'data':row['date_completed'],
                                        'produkt': line['parent_name'] if line['parent_name'] is not None else line['name'],
                                        'wariant': line['meta_data'][0].get('value') if line['meta_data'] != [] else None
                                        }, index=[line['id']])

                basic_orders_data = pd.concat([basic_orders_data, new_series], axis=0)

        basic_orders_data['cena'] =  pd.to_numeric(basic_orders_data['cena'])
        
        return basic_orders_data