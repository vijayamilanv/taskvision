import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskvision.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

demo_users = [
    {
        'username': 'po_demo',
        'email': 'po@example.com',
        'password': '123456',
        'first_name': 'Demo',
        'last_name': 'PO',
        'role': 'PO'
    },
    {
        'username': 'pm_demo',
        'email': 'pm@example.com',
        'password': '123456',
        'first_name': 'Demo',
        'last_name': 'PM',
        'role': 'PM'
    },
    {
        'username': 'tm_demo',
        'email': 'tm@example.com',
        'password': '123456',
        'first_name': 'Demo',
        'last_name': 'TM',
        'role': 'TM'
    }
]

for user_data in demo_users:
    if not User.objects.filter(email=user_data['email']).exists():
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            role=user_data['role']
        )
        print(f"Created demo user: {user_data['email']}")
    else:
        print(f"Skipping: {user_data['email']} already exists.")
