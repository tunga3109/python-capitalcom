from config import *
from capitalcom.client_demo import *

cl = Client(
    log=login,
    pas=password,
    api_key=API_KEY
)

w = cl.all_positions()
print(w)
