
import os
from dotenv import load_dotenv

env_file = '.env'
load_dotenv(env_file)

class Config:
    
    USER_NAME = os.environ.get('username')
    API_PASSWORD = os.environ.get('password')
    SHOP_URL = os.environ.get('shop_url')