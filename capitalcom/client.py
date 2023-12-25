from enum import Enum
import requests
import json

class CapitalComConstants():
    HEADER_API_KEY_NAME = 'X-CAP-API-KEY'
    API_VERSION = 'v1'
    BASE_URL = 'https://api-capital.backend-capital.com/api/{}/'.format(
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

class Client():
    """
    This is API for market Capital.com
    list of endpoints here : https://open-api.capital.com
    API documantation here: https://capital.com/api-development-guide
    """

    """Starting session"""
    def __init__(self, log, pas, api_key):
        self.login = log
        self.password = pas
        self.api_key = api_key

        self.session = requests.Session()
        self.response = self.session.post(
            CapitalComConstants.SESSION_ENDPOINT,
            json={'identifier': self.login, 'password': self.password},
            headers={'X-CAP-API-KEY': self.api_key}
        )
        if self.response.status_code == 200:
            self.cst = self.response.headers['CST']
            self.x_security_token = self.response.headers['X-SECURITY-TOKEN']
            # print(f'Status code: {self.response.status_code} - Successfully')
        else:
            print(f'Status code: {self.response.status_code} - {self.response.json()}')

    """Rest API Methods"""

    def _get(self, url, **kwargs):
        return requests.get(url, **kwargs)

    def _get_with_headers(self, url, **kwargs):
        return requests.get(url, **kwargs, headers=self._get_headers())

    def _get_with_params_and_headers(self, url, **kwargs):
        return requests.get(url, params=self._get_params(**kwargs), headers=self._get_headers())

    def _post(self, url, **kwargs):
        return requests.post(url, 
                                json=self._get_body_parameters(**kwargs),
                                headers=self._get_headers())

    def _delete(self, url, **kwargs):
        return requests.delete(url,
                            json=self._get_body_parameters(**kwargs),
                            headers=self._get_headers())

    def _put(self, url, **kwargs):
        return requests.put(url,
                            json=self._get_body_parameters(**kwargs),
                            headers=self._get_headers())

    """Headers"""
    def _get_headers(self, **kwargs):
        return {
                **kwargs,
                'CST': self.cst,
                'X-SECURITY-TOKEN': self.x_security_token
            }

    """Body Parameters"""
    def _get_body_parameters(self, **kwargs):
    
        return {
            **kwargs
            }

    """Params"""
    def _get_params(self, **kwargs):
        return {
            **kwargs
            }

    """SESSION"""
    def get_sesion_details(self): 
        """
        Returns the user's session details
        {
        "clientId": "12345678",
        "accountId": "12345678901234567",
        "timezoneOffset": 3,
        "locale": "en",
        "currency": "USD",
        "streamEndpoint": "wss://api-streaming-capital.backend-capital.com/"
        }
        """
        r = self._get_with_headers(
            CapitalComConstants.SESSION_ENDPOINT,
        )

        return json.loads(json.dumps(r.json(), indent=4))

    def switch_account(self, accountId): 
        """
        Switch active account
        {
        "trailingStopsEnabled": false,
        "dealingEnabled": true,
        "hasActiveDemoAccounts": false,
        "hasActiveLiveAccounts": true
        }
        """
        r = self._put(
            CapitalComConstants.SESSION_ENDPOINT,
            accountId=accountId,
        )
        return json.loads(json.dumps(r.json(), indent=4))

    def log_out_account(self):
        r = self._delete(
            CapitalComConstants.SESSION_ENDPOINT,
        )
        return json.loads(json.dumps(r.json(), indent=4))
    
    """ACCOUNTS"""
    def all_accounts(self): 
        """
        {
        "accounts": [
        {
        "accountId": "12345678901234567",
        "accountName": "USD",
        "status": "ENABLED",
        "accountType": "CFD",
        "preferred": true,
        "balance": {
            "balance": 124.95,
            "deposit": 125.18,
            "profitLoss": -0.23,
            "available": 116.93
        },
        "currency": "USD"
        },
        {
        "accountId": "12345678907654321",
        "accountName": "Second account",
        "status": "ENABLED",
        "accountType": "CFD",
        "preferred": false,
        "balance": {
            "balance": 100,
            "deposit": 100,
            "profitLoss": 0,
            "available": 0
            },
        "currency": "USD"
         }
        ]
        }
        """
        r = self._get_with_headers(
            CapitalComConstants.ACCOUNTS_ENDPOINT,
        )
        return json.loads(json.dumps(r.json(), indent=4))


    def account_preferences(self): 
        r = self._get_with_headers(
            CapitalComConstants.ACCOUNT_PREFERENCES_ENDPOINT,
        )
        return json.loads(json.dumps(r.json(), indent=4))


    def update_account_preferences(self,hedgingmode: bool, leverages: dict = None): 
        r = self._put(
            CapitalComConstants.ACCOUNT_PREFERENCES_ENDPOINT,
            leverages=leverages,
            hedgingMode=hedgingmode
        )
        return json.loads(json.dumps(r.json(), indent=4))


    def account_activity_history(self, 
                                    fr: str = None, 
                                    to: str = None, 
                                    last_period: int = 600, 
                                    detailed: bool = True, 
                                    dealid: str = None, 
                                    epic: str = None, 
                                    filter: str = None): 
        
        f = 'from'
        r = self._get_with_params_and_headers(
            CapitalComConstants.ACCOUNT_ACTIVITY_HISTORY_ENDPOINT,
            f=fr,
            to=to,
            lastPeriod=last_period,
            detailed=detailed,
            dealId=dealid,
            epic=epic,
            filter=filter
        )
        return json.loads(json.dumps(r.json(), indent=4))
    
    def account_transactions_history(self):
        r = self._get_with_headers(
            CapitalComConstants.ACCOUNT_TRANSACTIONS_ENDPOINT
        )

        return json.loads(json.dumps(r.json(), indent=4))

    """POSITIONS"""
    def position_order_confirmation(self, deal_reference: str):   
        r = self._get_with_headers(
            CapitalComConstants.ACCOUNT_ORDER_CONFIRMATION + '/' + deal_reference,
        )
        return json.loads(json.dumps(r.json(), indent=4))

    def all_positions(self):   
        r = self._get_with_headers(
            CapitalComConstants.POSITIONS_ENDPOINT,
        )
        return json.loads(json.dumps(r.json(), indent=4))

    def place_the_position(self, 
                            direction: DirectionType, 
                            epic: str, 
                            size: float, 
                            gsl: bool = False, 
                            tsl: bool = False, 
                            stop_level: float = None, 
                            stop_distance: float = None, 
                            stop_amount: float = None, 
                            profit_level: float = None, 
                            profit_distance: float = None, 
                            profit_amount: float = None):

        r = self._post(
            CapitalComConstants.POSITIONS_ENDPOINT,
            direction=direction.value,
            epic=epic,
            size=size,
            guaranteedStop=gsl,
            trailingStop=tsl,
            stopLevel=stop_level,
            stopDistance=stop_distance,
            stopAmount=stop_amount,
            profitLevel=profit_level,
            profitDistance=profit_distance,
            profitAmount=profit_amount
        )
        return json.loads(json.dumps(r.json(), indent=4))


    def check_position(self, dealid: str):
        r = self._get_with_headers(
            CapitalComConstants.POSITIONS_ENDPOINT + '/' + dealid,
        )
        return json.loads(json.dumps(r.json(), indent=4))


    def update_the_position(self, 
                            dealid: str,
                            gsl: bool = False, 
                            tsl: bool = False, 
                            stop_level: float = None, 
                            stop_distance: float = None, 
                            stop_amount: float = None, 
                            profit_level: float = None, 
                            profit_distance: float = None, 
                            profit_amount: float = None
                            ):
        r = self._put(
            CapitalComConstants.POSITIONS_ENDPOINT + '/' + dealid,
            guaranteedStop=gsl,
            trailingStop=tsl,
            stopLevel=stop_level,
            stopDistance=stop_distance,
            stopAmount=stop_amount,
            profitLevel=profit_level,
            profitDistance=profit_distance,
            profitAmount=profit_amount
        )
        return json.loads(json.dumps(r.json(), indent=4))

    
    def close_position(self, dealid): 
        r = self._delete(
            CapitalComConstants.POSITIONS_ENDPOINT,
            dealId=dealid,
        )
        return json.dumps(r.json(), indent=4)

    """ORDER"""
    def all_orders(self):   
        r = self._get_with_headers(
            CapitalComConstants.ORDERS_ENDPOINT,
        )
        return json.loads(json.dumps(r.json(), indent=4))


    def place_the_order(self, 
                            direction: DirectionType, 
                            epic: str, 
                            size: float, 
                            level: float,
                            type: OrderType,
                            gsl: bool = False, 
                            tsl: bool = False, 
                            good_till_date: str = None,
                            stop_level: float = None, 
                            stop_distance: float = None, 
                            stop_amount: float = None, 
                            profit_level: float = None, 
                            profit_distance: float = None, 
                            profit_amount: float = None):

        r = self._post(
            CapitalComConstants.ORDERS_ENDPOINT,
            direction=direction.value,
            epic=epic,
            size=size,
            level=level,
            type=type.value,
            goodTillDate=good_till_date,
            guaranteedStop=gsl,
            trailingStop=tsl,
            stopLevel=stop_level,
            stopDistance=stop_distance,
            stopAmount=stop_amount,
            profitLevel=profit_level,
            profitDistance=profit_distance,
            profitAmount=profit_amount
        )
        return json.loads(json.dumps(r.json(), indent=4))

    
    def update_the_order(self, 
                            level: float = None,
                            good_till_date: str = None,
                            gsl: bool = False, 
                            tsl: bool = False, 
                            stop_level: float = None, 
                            stop_distance: float = None, 
                            stop_amount: float = None, 
                            profit_level: float = None, 
                            profit_distance: float = None, 
                            profit_amount: float = None):

        r = self._put(
            CapitalComConstants.ORDERS_ENDPOINT,
            level=level,
            goodTillDate=good_till_date,
            guaranteedStop=gsl,
            trailingStop=tsl,
            stopLevel=stop_level,
            stopDistance=stop_distance,
            stopAmount=stop_amount,
            profitLevel=profit_level,
            profitDistance=profit_distance,
            profitAmount=profit_amount
        )
        return json.loads(json.dumps(r.json(), indent=4))
    
    
    def close_order(self, dealid): 
        r = self._delete(
            CapitalComConstants.ORDERS_ENDPOINT + '/' + dealid,
        )
        return json.loads(json.dumps(r.json(), indent=4))
    

    def single_market(self, epic: str):
        r = self._get_with_headers(
            CapitalComConstants.MARKET_INFORMATION_ENDPOINT + '/' + epic
        )
        return json.loads(json.dumps(r.json(), indent=4))
    
    def market_navigation(self, node_id: str = ''):
        r = self._get_with_headers(
            CapitalComConstants.MARKET_NAVIGATION_ENDPOINT + '/' + node_id
        )
        return json.loads(json.dumps(r.json(), indent=4))
    

    def searching_market(self, searchTerm: str = None, epics: str = None):
        r = self._get_with_params_and_headers(
                CapitalComConstants.MARKET_INFORMATION_ENDPOINT,
                searchTerm=searchTerm,
                epics=epics
        )
        return json.loads(json.dumps(r.json(), indent=4))
    
    def historical_price(self, epic, resolution:ResolutionType = ResolutionType.MINUTE, max:int = 10, fr:str = None, to:str = None):

        r = self.session.get(
            CapitalComConstants.PRICES_INFORMATION_ENDPOINT + '/' + epic,
            params={
                'resolution': resolution.value,
                'max': max,
                'from': fr,
                'to': to
            },
            headers={
                'CST': self.cst,
                'X-SECURITY-TOKEN': self.x_security_token
            }
        )
        return json.loads(json.dumps(r.json(), indent=4))

    def watchlist(self, watchlist_id:str=''):

        r = self._get_with_headers(
            CapitalComConstants.WATCHLISTS_ENDPOINT + '/' + watchlist_id
        )

        return json.loads(json.dumps(r.json(), indent=4))
    
    def check_server_time(self):
        r = self._get(
            CapitalComConstants.SERVER_TIME_ENDPOINT
        )
        return json.loads(json.dumps(r.json(), indent=4))
    
    def client_sentiment(self):
        r = self._get_with_headers(
            CapitalComConstants.CLIENT_SENTIMENT_ENDPOINT
        )
        return json.loads(json.dumps(r.json(), indent=4))

    def margin_calculation(self, price: float, leverage: float, size: float):
        
        return (price * size) * 1/leverage
    
    def overnight_fee_calculation(self, 
                                  closing_ask: float, 
                                  closing_bid: float, 
                                  size: float,
                                  fee_rate: float):
        mid_price = (closing_ask + closing_bid)/2
        overnight_fee = round(mid_price * size * fee_rate, 2)

        return overnight_fee
    
    def topping_up_funds(self, amount: float):

        if -40000 <= amount <= 40000: 
            r = self._post(
                CapitalComConstants.TOPPING_UP_ENDPOINT,
                amount=amount
            )
            return json.loads(json.dumps(r.json(), indent=4))
        
        else:
            return {"errorCode": "error.invalid.amount"}

