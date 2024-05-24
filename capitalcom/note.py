from config import login, password, API_KEY
import time
from client_demo import *

cl = Client(login, password, API_KEY)

pos = cl.place_the_position(
    direction=DirectionType.BUY,
    epic='BTCUSD',
    size=1
)

a = ''