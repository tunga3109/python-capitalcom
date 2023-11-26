from capitalcom.client_demo import Client
from capitalcom.config import API_KEY, login, password


cl = Client(
    login,
    password,
    API_KEY
)

price = cl.historical_prices(
    'BTCUSD'
)

a = ''