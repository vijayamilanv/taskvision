import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskvision.settings')
django.setup()

from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
User = get_user_model()

user = User.objects.get(email='po@example.com')
token = Token.objects.get(user=user)
print(f"User: {user.email}")
print(f"Token: {token.key}")
print(f"Token Hex: {''.join(hex(ord(c)) for c in token.key)}")
