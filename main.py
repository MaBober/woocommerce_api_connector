
import datetime as dt
from config import Config

from WooAPIConnector import WooShop


url = Config.SHOP_URL
user = Config.USER_NAME
password = Config.API_PASSWORD

my_shop = WooShop(url, user, password)
orders_df = my_shop.get_basic_orders_data(after=dt.datetime.today() - dt.timedelta(days=150), only_completed=False)

