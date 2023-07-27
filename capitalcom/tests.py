import unittest
import warnings


from client_demo import *
from config import *

class TestCapitalAPI(unittest.TestCase):

    def setUp(self) -> None:
        
        self.client = Client(login, password, API_KEY)

    def test_status_code(self):

        self.status_code = self.client.response.status_code
        self.assertEqual(self.status_code, 200)

        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

    def test_account_info(self):
        self.account_info = self.client.all_accounts()
        self.assertEqual(self.account_info, self.account_info)

        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

    def test_placing_position(self):
        self.placing_position = self.client.place_the_position(
            epic='BTCUSD',
            size=1,
            direction=DirectionType.BUY
        )
        self.assertEqual(self.placing_position, self.placing_position)

        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)


    def test_marketnavigation(self):
        self.market_nav = self.client.market_navigation()
        self.assertEqual(self.market_nav, self.market_nav)

        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)



if __name__ == '__main__':
   
    unittest.main()




