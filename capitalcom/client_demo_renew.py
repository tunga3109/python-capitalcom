from enum import Enum
from abc import ABC, abstractmethod
import requests
import json

class CapitalComConstants():
    HEADER_API_KEY_NAME = 'X-CAP-API-KEY'
    API_VERSION = 'v1'
    BASE_URL = 'https://demo-api-capital.backend-capital.com/api/{}/'.format(
        API_VERSION
    )

    SERVER_TIME_ENDPOINT = BASE_URL + 'time'
    PING_INFORMATION_ENDPOINT = BASE_URL + 'ping'

    SESSION_ENDPOINT = BASE_URL + 'session'
    ENCRYPTION_KEY_ENDPOINT = SESSION_ENDPOINT + '/' + 'encryptionKey'

    ACCOUNTS_ENDPOINT = BASE_URL + 'accounts'
    ACCOUNT_PREFERENCES_ENDPOINT = ACCOUNTS_ENDPOINT + '/' + 'preferences'
    TOPPING_UP_ENDPOINT = ACCOUNTS_ENDPOINT + '/' + 'topUp'

    ACCOUNT_HISTORY_ENDPOINT = BASE_URL + 'history'
    ACCOUNT_ACTIVITY_HISTORY_ENDPOINT = ACCOUNT_HISTORY_ENDPOINT + '/' + 'activity'
    ACCOUNT_TRANSACTIONS_ENDPOINT = ACCOUNT_HISTORY_ENDPOINT + '/' + 'transactions'

    ACCOUNT_ORDER_CONFIRMATION = BASE_URL + 'confirms'
    POSITIONS_ENDPOINT = BASE_URL + 'positions'
    ORDERS_ENDPOINT = BASE_URL + 'workingorders'

    MARKET_NAVIGATION_ENDPOINT = BASE_URL + 'marketnavigation'
    MARKET_INFORMATION_ENDPOINT = BASE_URL + 'markets'

    PRICES_INFORMATION_ENDPOINT = BASE_URL + 'prices'

    CLIENT_SENTIMENT_ENDPOINT = BASE_URL + 'clientsentiment'

    WATCHLISTS_ENDPOINT = BASE_URL + 'watchlists'


class DirectionType(Enum):
    BUY = 'BUY'
    SELL = 'SELL'

class OrderType(Enum):
    LIMIT = 'LIMIT'
    STOP = 'STOP'

class SourceType(Enum):
    CLOSE_OUT = 'CLOSE_OUT'
    DEALER = 'DEALER'
    SL = 'SL'
    SYSTEM = 'SYSTEM'
    TP = 'TP'
    USER = 'USER'

class StatusType(Enum):
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    UNKNOWN = 'UNKNOWN'

class FilterType(Enum):
    EDIT_STOP_AND_LIMIT = 'EDIT_STOP_AND_LIMIT'
    POSITION = 'POSITION'
    SYSTEM = 'SYSTEM'
    WORKING_ORDER = 'WORKING_ORDER'

class TransationType(Enum):
    DEPOSIT = 'DEPOSIT'
    WITHDRAWAL = 'WITHDRAWAL'
    REFUND = 'REFUND'
    WITHDRAWAL_MONEY_BACK = 'WITHDRAWAL_MONEY_BACK'
    TRADE = 'TRADE'
    SWAP = 'SWAP'
    TRADE_COMMISSION = 'TRADE_COMMISSION'
    TRADE_COMMISSION_GSL = 'TRADE_COMMISSION_GSL'
    CONVERT = 'CONVERT'
    NEGATIVE_BALANCE_PROTECTION = 'NEGATIVE_BALANCE_PROTECTION'
    REIMBURSEMENT = 'REIMBURSEMENT'
    TRADE_CORRECTION = 'TRADE_CORRECTION'
    CHARGEBACK = 'CHARGEBACK'
    ADJUSTMENT = 'ADJUSTMENT'
    DIVIDEND = 'DIVIDEND'
    ACCOUNT_CLOSURE = 'ACCOUNT_CLOSURE'
    BONUS = 'BONUS'
    TRANSFER = 'TRANSFER'

class ResolutionType(Enum):
    MINUTE = 'MINUTE'
    MINUTE_5 = 'MINUTE_5'
    MINUTE_15 = 'MINUTE_15'
    MINUTE_30 = 'MINUTE_30'
    HOUR = 'HOUR'
    HOUR_4 = 'HOUR_4'
    DAY = 'DAY'
    WEEK = 'WEEK'
    
    
class APIClient(ABC):
    @abstractmethod
    def _get(self, url, **kwargs):
        pass

    @abstractmethod
    def _post(self, url, **kwargs):
        pass

    @abstractmethod
    def _put(self, url, **kwargs):
        pass

    @abstractmethod
    def _delete(self, url, **kwargs):
        pass
    
class CapitalComSession:
    def __init__(self, log, pas, api_key):
        self.session = requests.Session()
        self.api_key = api_key
        self.cst, self.x_security_token = self._authenticate(log, pas)

    def _authenticate(self, login, password):
        response = self.session.post(
            CapitalComConstants.SESSION_ENDPOINT,
            json={'identifier': login, 'password': password},
            headers={'X-CAP-API-KEY': self.api_key}
        )
        if response.status_code == 200:
            cst = response.headers['CST']
            x_security_token = response.headers['X-SECURITY-TOKEN']
            return cst, x_security_token
        else:
            raise Exception(f"Authentication failed: {response.status_code} - {response.json()}")

    def get_headers(self, **kwargs):
        return {
            **kwargs,
            'CST': self.cst,
            'X-SECURITY-TOKEN': self.x_security_token
        }

    def close(self):
        self.session.close()
        
class CapitalComClient(APIClient):
    def __init__(self, session: CapitalComSession):
        self.session = session

    def _get(self, url, **kwargs):
        return requests.get(url, **kwargs)

    def _post(self, url, **kwargs):
        return requests.post(url, json=kwargs.get('json'), headers=self.session.get_headers())

    def _put(self, url, **kwargs):
        return requests.put(url, json=kwargs.get('json'), headers=self.session.get_headers())

    def _delete(self, url, **kwargs):
        return requests.delete(url, json=kwargs.get('json'), headers=self.session.get_headers())
    

class AccountService:
    def __init__(self, client: APIClient):
        self.client = client

    def all_accounts(self):
        response = self.client._get(CapitalComConstants.ACCOUNTS_ENDPOINT, headers=self.client.session.get_headers())
        return self._process_response(response)

    def account_preferences(self):
        response = self.client._get(CapitalComConstants.ACCOUNT_PREFERENCES_ENDPOINT, headers=self.client.session.get_headers())
        return self._process_response(response)
    
    def update_account_preferences(self, hedging_mode: bool, leverages: dict = None):
        payload = {
            "hedgingMode": hedging_mode
        }
        if leverages:
            payload["leverages"] = leverages

        response = self.client._put(CapitalComConstants.ACCOUNT_PREFERENCES_ENDPOINT, json=payload)
        return self._process_response(response)
    
    def account_activity_history(self, fr: str = None, to: str = None, last_period: int = 600,
                                detailed: bool = True, deal_id: str = None, epic: str = None, filter: str = None):
        params = {
            'from': fr,
            'to': to,
            'lastPeriod': last_period,
            'detailed': detailed,
            'dealId': deal_id,
            'epic': epic,
            'filter': filter
        }
        response = self.client._get(CapitalComConstants.ACCOUNT_ACTIVITY_HISTORY_ENDPOINT, params=params,
                                    headers=self.client.session.get_headers())
        return self._process_response(response)
    
    def account_transactions_history(self):
        response = self.client._get(CapitalComConstants.ACCOUNT_TRANSACTIONS_ENDPOINT,
                                    headers=self.client.session.get_headers())
        return self._process_response(response)


    @staticmethod
    def _process_response(response):
        if response.status_code == 200:
            return json.loads(json.dumps(response.json(), indent=4))
        else:
            return {"error": response.status_code, "message": response.json()}
        
class PositionService:
    def __init__(self, client: APIClient):
        self.client = client

    def position_order_confirmation(self, deal_reference: str):
        response = self.client._get(CapitalComConstants.ACCOUNT_ORDER_CONFIRMATION + '/' + deal_reference,
                                    headers=self.client.session.get_headers())
        return self._process_response(response)

    def all_positions(self):
        response = self.client._get(CapitalComConstants.POSITIONS_ENDPOINT, headers=self.client.session.get_headers())
        return self._process_response(response)

    def place_the_position(self, direction: DirectionType, epic: str, size: float, gsl: bool = False, tsl: bool = False,
                           stop_level: float = None, stop_distance: float = None, stop_amount: float = None,
                           profit_level: float = None, profit_distance: float = None, profit_amount: float = None):
        payload = {
            "direction": direction.value,
            "epic": epic,
            "size": size,
            "guaranteedStop": gsl,
            "trailingStop": tsl,
            "stopLevel": stop_level,
            "stopDistance": stop_distance,
            "stopAmount": stop_amount,
            "profitLevel": profit_level,
            "profitDistance": profit_distance,
            "profitAmount": profit_amount
        }
        response = self.client._post(CapitalComConstants.POSITIONS_ENDPOINT, json=payload)
        return self._process_response(response)

    def update_the_position(self, dealid: str, gsl: bool = False, tsl: bool = False, stop_level: float = None,
                            stop_distance: float = None, stop_amount: float = None, profit_level: float = None,
                            profit_distance: float = None, profit_amount: float = None):
        payload = {
            "guaranteedStop": gsl,
            "trailingStop": tsl,
            "stopLevel": stop_level,
            "stopDistance": stop_distance,
            "stopAmount": stop_amount,
            "profitLevel": profit_level,
            "profitDistance": profit_distance,
            "profitAmount": profit_amount
        }
        response = self.client._put(CapitalComConstants.POSITIONS_ENDPOINT + '/' + dealid, json=payload)
        return self._process_response(response)

    def close_position(self, dealid):
        response = self.client._delete(CapitalComConstants.POSITIONS_ENDPOINT, json={"dealId": dealid})
        return self._process_response(response)

    @staticmethod
    def _process_response(response):
        if response.status_code == 200:
            return json.loads(json.dumps(response.json(), indent=4))
        else:
            return {"error": response.status_code, "message": response.json()}

class OrderService:
    def __init__(self, client: APIClient):
        self.client = client

    def all_orders(self):
        response = self.client._get(CapitalComConstants.ORDERS_ENDPOINT, headers=self.client.session.get_headers())
        return self._process_response(response)

    def place_the_order(self, direction: DirectionType, epic: str, size: float, level: float, order_type: str,
                        gsl: bool = False, tsl: bool = False, good_till_date: str = None, stop_level: float = None,
                        stop_distance: float = None, stop_amount: float = None, profit_level: float = None,
                        profit_distance: float = None, profit_amount: float = None):
        payload = {
            "direction": direction.value,
            "epic": epic,
            "size": size,
            "level": level,
            "type": order_type,
            "goodTillDate": good_till_date,
            "guaranteedStop": gsl,
            "trailingStop": tsl,
            "stopLevel": stop_level,
            "stopDistance": stop_distance,
            "stopAmount": stop_amount,
            "profitLevel": profit_level,
            "profitDistance": profit_distance,
            "profitAmount": profit_amount
        }
        response = self.client._post(CapitalComConstants.ORDERS_ENDPOINT, json=payload)
        return self._process_response(response)

    def close_order(self, dealid):
        response = self.client._delete(CapitalComConstants.ORDERS_ENDPOINT + '/' + dealid)
        return self._process_response(response)

    @staticmethod
    def _process_response(response):
        if response.status_code == 200:
            return json.loads(json.dumps(response.json(), indent=4))
        else:
            return {"error": response.status_code, "message": response.json()}
        
class MarketService:
    def __init__(self, client: APIClient):
        self.client = client

    def single_market(self, epic: str):
        response = self.client._get(
            CapitalComConstants.MARKET_INFORMATION_ENDPOINT + '/' + epic,
            headers=self.client.session.get_headers()
        )
        return self._process_response(response)

    def market_navigation(self, node_id: str = ''):
        response = self.client._get(
            CapitalComConstants.MARKET_NAVIGATION_ENDPOINT + '/' + node_id,
            headers=self.client.session.get_headers()
        )
        return self._process_response(response)

    def searching_market(self, searchTerm: str = None, epics: str = None):
        params = {
            'searchTerm': searchTerm,
            'epics': epics
        }
        response = self.client._get(
            CapitalComConstants.MARKET_INFORMATION_ENDPOINT,
            params=params,
            headers=self.client.session.get_headers()
        )
        return self._process_response(response)

    def historical_price(self, epic: str, resolution: ResolutionType = ResolutionType.MINUTE, max: int = 10, fr: str = None, to: str = None):
        params = {
            'resolution': resolution.value,
            'max': max,
            'from': fr,
            'to': to
        }
        response = self.client._get(
            CapitalComConstants.PRICES_INFORMATION_ENDPOINT + '/' + epic,
            params=params,
            headers=self.client.session.get_headers()
        )
        return self._process_response(response)

    @staticmethod
    def _process_response(response):
        if response.status_code == 200:
            return json.loads(json.dumps(response.json(), indent=4))
        else:
            return {"error": response.status_code, "message": response.json()}





