import requests
import datetime as dt
import pandas as pd


class WooShop:
    """
    A class represnting WooCommerce shop.

    Attributes
    ----------
    url : str
        URL address of shop to connect.
    user : str
        User key generated in WooCommerce REST API settings.
    secret_key : str
        Secret key generated in WooCommerce REST API settings.
    
        
    Methods
    ----------
    get_raw_orders(after, before = dt.datetime.today())
        Returns all data of orders placed between passed dates in JSON format.
    get_basic_orders_data(after, before = dt.datetime.today(), only_completed=True)
        Returns basic information about orders placed between passed dates in Pandas Dataframe.
    """

    #TODO: Move to settings file.
    requests_data = {
    'orders' : 'wp-json/wc/v3/orders',
    'customers' : '/wp-json/wc/v3/customers'
    }


    def __init__(self, shop_url, user, secret_key) -> None:
        """Constructor

        Parameters
        ----------
        url : str
            URL address of shop to connect.
        user : str
            User key generated in WooCommerce REST API settings.
        secret_key : str
            Secret key generated in WooCommerce REST API settings.
        """

        self.url = shop_url
        self.user = user
        self.secret_key = secret_key

    
    def __send_GET_request(self, request_scope, *additional_parameters):
        """Sends GET request to WooCommerce shop. 

        Implements pagination handling. All pages are added to one list.
        Additional paramaters to request can be provided by argument.

        Parameters
        ---------- 
        request_scope : str
            Woocoomerce URL for specfic request. 
        *additional_parameters: dict
            Dictionary containing additional parameters for GET request.

        Returns
        -------
        list
            Full response recivied from API, all pages aggregated to list.
        """

        page_nr = 1
        total_response = []

        requests_parameters = {
            'per_page': 20,
            'page': page_nr
        }

        for parameter in additional_parameters:
            requests_parameters.update(parameter)

        while True:
            
            page_response = requests.get(self.url + request_scope,
                params=requests_parameters,
                auth=(self.user, self.secret_key))

            if len(page_response.json()) == 0:
                break

            total_response.extend(page_response.json())
            requests_parameters['page'] += 1

        return total_response


    def get_raw_orders(self, after: dt.datetime, before: dt.datetime = dt.datetime.today()) -> list:
        """Returns all data of orders placed between passed dates in JSON format.

        Parameters
        ----------
        after : dt.datetime
            Defines date of first order which will be collected.
        before : dt.datetime, optional
            Defines date of last order which will be collected, by default dt.datetime.today()

        Returns
        -------
        list
            List of all data about selected orders in JSON style format.
        """
    
        additional_parameters = {
                'after': after.isoformat(),
                'before': before.isoformat()}
        
        total_response = self.__send_GET_request(WooShop.requests_data['orders'], additional_parameters)
    
        return total_response

    def get_raw_customers(self):
        """Returns all data customers in JSON format.

        Returns
        -------
        list
            List of all data about all customers in JSON style format.
        """

        total_response = self.__send_GET_request(WooShop.requests_data['customers'])
    
        return total_response

    
    #TODO: split to whole orders version and divided for single lines.
    def get_basic_orders_data(self, after: dt.datetime, before: dt.datetime = dt.datetime.today(), only_completed=True) -> pd.DataFrame :
        """Returns basic information about orders .

        Orders to analyze can be limited by dates range.
        Multi-position orders are divided to single products.
        Data included in returned DataFrame:
            - line ID,
            - price,
            - customer ID,
            - order completion date
            - product name
            - product variant


        Parameters
        ----------
        after : dt.datetime
            Defines date of first order which will be collected.
        before : dt.datetime, optional
            Defines date of last order which will be collected, by default dt.datetime.today()
        only_completed : bool, optional
            If True, not completed orders will be exluded from returned data set, by default True.

        Returns
        -------
        pd.DataFrame
            DataFrame with orders data.
        """

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