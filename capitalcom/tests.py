from client import *
from requests import *

cl = Client(login, password, API_KEY)
print(cl.close_position(dealid='000940dd-0055-311e-0000-00008177e2f4'))
