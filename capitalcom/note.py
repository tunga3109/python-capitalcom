from config import login, password, API_KEY

from client_demo import *

cl = Client(
    login,
    password,
    API_KEY
)

prices = cl.check_server_time()

a = ''