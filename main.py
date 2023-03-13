from dotenv import load_dotenv
import requests
import os
from pprint import pprint


def send_request():

    user = os.environ.get('username')
    password = os.environ.get('password')

    response = requests.get('https://www.skorskadietetyk.com/wp-json/wc/v2/orders?before=2023-01-01T14:10:20', auth=(user, password))
    pprint(type(response.json()))



env_file = '.env'
load_dotenv(env_file)

send_request()





