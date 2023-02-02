from client import *
from config import *

import requests


cl = Client(login, password, API_KEY)
print(cl.account_activity_history(fr='2021-11-20T00:00:00', to='2022-06-30T00:00:00', filter='source!={0};type!={1};status=={2};'.format(SourceType.SL, FilterType.POSITION, StatusType.ACCEPTED)))




