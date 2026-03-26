import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskvision.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

demo_users = [
    {
        'username': 'po@example.com',
        'email': 'po@example.com',
        'role': 'PO'
    },
    {
        'username': 'pm@example.com',
        'email': 'pm@example.com',
        'role': 'PM'
    },
    {
        'username': 'tm@example.com',
        'email': 'tm@example.com',
        'role': 'TM'
    }
]

for ud in demo_users:
    user = User.objects.filter(email=ud['email']).first()
    if user:
        user.username = ud['username']
        user.set_password('123456')
        user.save()
        print(f"Updated {ud['email']}")
    else:
        user = User.objects.create_user(
            username=ud['username'],
            email=ud['email'],
            password='123456',
            role=ud['role']
        )
        print(f"Created {ud['email']}")
