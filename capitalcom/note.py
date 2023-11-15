from config import login, password, API_KEY
from capitalcom.client_demo import Client


cl = Client(
    login,
    password,
    API_KEY
)

prices = cl.historical_prices(
    epic='BTCUSD'
)

print(cl.cst)

a = ''


