from client import *
from config import *

import requests


cl = Client(login, password, API_KEY)


r = requests.post(
    CapitalComConstants.SESSION_ENDPOINT,
    json={'identifier': login, 'password': password},
    headers={'X-CAP-API-KEY': API_KEY}
)
print(r.status_code)





