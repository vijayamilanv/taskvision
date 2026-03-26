import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskvision.settings')
django.setup()

from django.conf import settings
print(settings.DATABASES['default'])
