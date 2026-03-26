import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskvision.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute('DESCRIBE core_task')
    for row in cursor.fetchall():
        print(row)
