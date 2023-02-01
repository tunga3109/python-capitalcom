from datetime import datetime, timedelta
from enum import Enum

import requests

from config import *

class CapitalComConstants():
    HEADER_API_KEY_NAME = 'X-CAP-API-KEY'
    API_VERSION = 'v1'
    BASE_URL = 'https://demo-api-capital.backend-capital.com/api/{}/'.format(
        API_VERSION
    )
    BASE_DEMO_URL = 'https://demo-api-capital.backend-capital.com/api/{}/'.format(
        API_VERSION
    )

    SERVER_TIME_ENDPOINT = BASE_URL + 'time'
    PING_INFORMATION_ENDPOINT = BASE_URL + 'ping'

    SESSION_ENDPOINT = BASE_URL + 'session'
    ENCRYPTION_KEY_ENDPOINT = SESSION_ENDPOINT + '/' + 'encryptionKey'

    ACCOUNTS_ENDPOINT = BASE_URL + 'accounts'
    ACCOUNT_PREFERENCES_ENDPOINT = ACCOUNTS_ENDPOINT + '/' + 'preferences'

    ACCOUNT_HISTORY_ENDPOINT = BASE_URL + 'history'
    ACCOUNT_ACTIVITY_HISTORY_ENDPOINT = ACCOUNT_HISTORY_ENDPOINT + '/' + 'activity'
    ACCOUNT_TRANSACTION_HISTORY_ENDPOINT = ACCOUNT_HISTORY_ENDPOINT + '/' + 'transactions'

    POSITIONS_ENDPOINT = BASE_URL + 'positions'
    ORDERS_ENDPOINT = BASE_URL + 'workingorders'

    MARKET_NAVIGATION_ENDPOINT = BASE_URL = 'marketnavigation'
    MARKET_INFORMATION_ENDPOINT = BASE_URL + 'markets'

    PRICES_INFORMATION_ENDPOINT = BASE_URL + 'prices'

    CLIENT_SENTIMENT_ENDPOINT = BASE_URL + 'clientsentiment'

    WATCHLISTS_ENDPOINT = BASE_URL + 'watchlists'


class DirectionType(Enum):
    BUY = 'BUY'
    SELL = 'SELL'
    
class StopLossType(Enum):
    LEVEL = 'stopLevel'
    DISTANCE = 'stopDistance'
    AMOUNT = 'stopAmount'
    GUARANTEED = 'guaranteedStop'
    TRAILING = 'trailingStop'
    
class TakeProfitType(Enum):
    LEVEL = 'profitLevel'
    DISTANCE = 'profitDistance'
    AMOUNT = 'profitAmount'

key = 'kdkjekjdsjkdkjd'


class Client():
    """
    This is API for market Capital.com
    list of endpoints here : https://open-api.capital.com
    API documantation here: https://capital.com/api-development-guide
    """

    def __init__(self, login, password, api_key):
        self.login = login
        self.password = password
        self.api_key = api_key


    
    def _get_header(self, **kwargs):
        return {
            **kwargs
        }

    def _get(self, url, **kwargs):
        return requests.get(url, **kwargs)

    def _post(self, url, **kwargs):
        return requests.post(url, **kwargs)

    def _delete(self, url, **kwargs):
        return requests.delete(url, **kwargs)

    def start_session(self):
        r = self._post(
            CapitalComConstants.SESSION_ENDPOINT, 
            json={'identifier': login, 'password': password},
            headers={CapitalComConstants.HEADER_API_KEY_NAME: self.api_key}
            )
        return r.json()
    
    def _get_cst(self) -> str:
        r = self._post(
            CapitalComConstants.SESSION_ENDPOINT, 
            json={'identifier': login, 'password': password},
            headers={CapitalComConstants.HEADER_API_KEY_NAME: self.api_key}
            )

        return r.headers['CST']

    def _get_x_security_token(self) -> str:
        r = self._post(
            CapitalComConstants.SESSION_ENDPOINT, 
            json={'identifier': login, 'password': password},
            headers={CapitalComConstants.HEADER_API_KEY_NAME: self.api_key}
            )

        return r.headers['X-SECURITY-TOKEN']

    
    def accounts_information(self, cst, x_token): #!!!!!!!!!!!!
        r = self._get(
            CapitalComConstants.SESSION_ENDPOINT,
            headers={
                'CST': cst,
                'X-SECURITY-TOKEN': x_token
            }
        )

        return r.json()





# cl = Client(login, password, API_KEY)

# c = cl._get_cst()
# x = cl._get_x_security_token()

# print(cl.accounts_information(cst='j4zKbE4dncy7SQH0pTg4v1NM', x_token='dBntDf8bsCiS76hDNElLmzpL5xh12nL'))










        







