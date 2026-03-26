import os
import sys
import django  # pyre-ignore

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskvision.settings')
django.setup()

from django.contrib.auth import get_user_model  # pyre-ignore
User = get_user_model()
from core.models import Project, Task  # pyre-ignore

def init_db():
    print("Flushing database...")
    # Using Django's command system
    from django.core.management import call_command  # pyre-ignore
    call_command('flush', interactive=False)
    
    print("Creating initial users...")
    
    # 1. Product Owner
    po_user = User.objects.create_user(
        username='po@example.com',
        email='po@example.com',
        password='123456',
        role=User.Role.PRODUCT_OWNER,
        company='Google DeepMind',
        industry='AI'
    )
    po_user.first_name = 'Alice'
    po_user.last_name = 'PO'
    po_user.save()
    print(f"Created PO: {po_user}")

    # 2. Project Manager
    pm_user = User.objects.create_user(
        username='pm@example.com',
        email='pm@example.com',
        password='123456',
        role=User.Role.PROJECT_MANAGER,
        specialization='Software Development',
        years_experience=10
    )
    pm_user.first_name = 'David'
    pm_user.last_name = 'PM'
    pm_user.save()
    print(f"Created PM: {pm_user}")

    # 3. Team Member
    tm_user = User.objects.create_user(
        username='tm@example.com',
        email='tm@example.com',
        password='123456',
        role=User.Role.TEAM_MEMBER,
        skills='Python, Django, React',
        experience_level='Senior'
    )
    tm_user.first_name = 'John'
    tm_user.last_name = 'TM'
    tm_user.save()
    print(f"Created TM: {tm_user}")

    # 4. Superuser
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='123456',
        role=User.Role.ADMIN
    )
    print(f"Created Superuser: {admin_user}")

    print("\nInitial database setup complete!")
    print("Login Credentials:")
    print("- Product Owner:   po@example.com / 123456")
    print("- Project Manager: pm@example.com / 123456")
    print("- Team Member:     tm@example.com / 123456")
    print("- Superuser:       admin / 123456")

if __name__ == '__main__':
    init_db()
