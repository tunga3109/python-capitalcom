from config import login, password, API_KEY

from client_demo import *

cl = Client(
    login,
    password,
    API_KEY
)

prices = cl.historical_prices('BTCUSD')
print(prices)

a = ''