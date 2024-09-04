from config import *
from client_demo import *

from client_demo_renew import *

session = CapitalComSession(log=login, pas=password, api_key=API_KEY)

    # Initialize client with the session
client = CapitalComClient(session=session)

# Create service instance
account_service = AccountService(client=client)

market_service = MarketService(client=client)

position_service = PositionService(client=client)

position_service.place_the_position(direction=DirectionType.BUY, epic='BTCUSD', size=1)

# Close session when done
session.close()

a = ''