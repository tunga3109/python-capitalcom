from datetime import datetime, timedelta
from enum import Enum

import requests

class CapitalComConstants():
    HEADER_API_KEY_NAME = 'X-CAP-API-KEY'
    API_VERSION = 'v1'
    BASE_URL = 'https://api-capital.backend-capital.com/api/{}/'.format(
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



class Client():
    """
    This is API for market Capital.com
    list of endpoints here : https://open-api.capital.com
    API documantation here: https://capital.com/api-development-guide
    """

    def __init__(self, api_key):
        self.api_key = api_key

    
    def _get_header(self, **kwargs):
        return {
            **kwargs,
            CapitalComConstants.HEADER_API_KEY_NAME: self.api_key
        }



        







