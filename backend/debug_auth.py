import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskvision.settings')
django.setup()

from rest_framework.authentication import TokenAuthentication
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token

token_key = "ec60fe3830eadee146549ee45c4d111a4ffee5561"
factory = APIRequestFactory()
request = factory.get('/api/tasks/', HTTP_AUTHORIZATION=f'Token {token_key}')

auth = TokenAuthentication()
try:
    user_auth = auth.authenticate(request)
    if user_auth:
        user, token = user_auth
        print(f"Authenticated as: {user.username}")
    else:
        print("Authentication failed: returned None")
except Exception as e:
    print(f"Authentication failed with error: {e}")
