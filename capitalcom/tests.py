from client_demo import *
from config import *

cl = Client(login, password, API_KEY)
cl.close_position(dealid='000940dd-0055-311e-0000-0000818fe41d')