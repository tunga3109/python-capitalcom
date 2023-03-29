from client_demo import *
from config import *

cl = Client(login, password, API_KEY)
print(cl.update_the_order(dealId='000940dd-0055-311e-0000-000081864126', level=28299))
