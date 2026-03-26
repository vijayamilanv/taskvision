import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskvision.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

credentials = [
    ('po@example.com', '123456'),
    ('pm@example.com', '123456'),
    ('tm@example.com', '123456'),
    ('po_dummy', '123456'),
    ('pm_jordan', '123456'),
    ('tm_sam', '123456'),
    ('jordan@example.com', '123456'),
    ('sam@example.com', '123456')
]

for identity, pwd in credentials:
    user = User.objects.filter(email=identity).first() or User.objects.filter(username=identity).first()
    if user:
        user.set_password(pwd)
        user.save()
        print(f"Reset password for {user.username} (Email: {user.email}) to 123456")
    else:
        print(f"User not found for identity: {identity}")
