from config import *
from client_demo import *

from client_demo_beta_version_2 import *


pos_setting = PositionDetails(login, password, API_KEY)

user_setting = UserSettings(login, password, API_KEY)
user_setting.topping_up_funds(1000)

pos_setting.place_the_position(epic='BTCUSD', size=1, direction=DirectionType.BUY)
# pos_setting.close_position('000940dd-0055-311e-0000-00008294a64b')

a = ''