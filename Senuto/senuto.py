import requests
import json

"""
Script load token to later authorization by other Scripts
"""

login_data = {'email': 'Your_Email', 'password': 'Your_password'}

r = requests.post('https://api.senuto.com//api/users/token.json', data=login_data)
token = json.loads(r.content)['data']['token']