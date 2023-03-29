from client_demo import *
from config import *

cl = Client(login, password, API_KEY)

lev_1 = int(input('first leverage: '))
lev_2 = int(input('second leverage: '))
print(cl.account_preferences())
print(cl.update_account_preferences({"CRYPTOCURRENCIES": lev_1}))

print(cl.place_the_position(direction=DirectionType.BUY, epic='BTCUSD', size=1))

print(cl.update_account_preferences({"CRYPTOCURRENCIES": lev_2}))
print(cl.account_preferences())