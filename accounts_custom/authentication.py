from importlib import import_module
import requests
from django.contrib.auth import get_user_model

User = get_user_model()

VERIFY_URL = 'https://www.google.com'
DOMAIN = 'localhost'

class CustomAuthenticationBackend(object):

    def authenticate(self, url, email):
        #requests = import_module('requests')
        response = requests.post(url, data=email)
        
        if response.ok and response.json()['status'] == 'okay':
            email = response.json()['email']
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                return User.objects.create(email=email)

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
            
        
