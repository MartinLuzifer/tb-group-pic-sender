from pprint import pprint

import requests as requests

URL = 'https://meow.senither.com/v1/random'

response = requests.get(url=URL)
print(response.text)
url = response.json()['data']['url']
print(url)

