from config import login, password, API_KEY
import time

def measure_time(func):
    def wrapper():
        start = time.time()
        func()
        end = time.time()
        print(f"Execution time: {end - start} seconds")
    return wrapper


from client_demo_beta_version import *

session = AccountDetails(
    login,
    password,
    API_KEY
)

@measure_time
def margin():
    print(UserSettings.margin_calculation(1,1,1))
    
margin()

a = ''