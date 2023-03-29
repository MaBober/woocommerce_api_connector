
import datetime as dt
from config import Config
from WooAPIConnector import WooShop

url = Config.SHOP_URL
user = Config.USER_NAME
password = Config.API_PASSWORD

my_shop = WooShop(url, user, password)

try:
    customers = my_shop.get_raw_customers()
    orders = my_shop.get_basic_orders_data(after=dt.datetime.today() - dt.timedelta(days=15), only_completed=False)
    products = my_shop.get_raw_products()
    
except Exception as e:
    print(f"ERROR: {e}")


