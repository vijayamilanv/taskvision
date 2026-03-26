import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskvision.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Project, Task, Notification

User = get_user_model()

def seed_data():
    print("Clearing old dummy data...")
    User.objects.exclude(is_superuser=True).delete()
    Project.objects.all().delete()
    
    print("Creating Users...")
    po = User.objects.create_user(username="sarah_po", email="sarah@corp.com", password="password123", role=User.Role.PRODUCT_OWNER, first_name="Sarah", last_name="Connor", company="TechCorp")
    pm1 = User.objects.create_user(username="david_pm", email="david@corp.com", password="password123", role=User.Role.PROJECT_MANAGER, first_name="David", last_name="Miller", specialization="Agile")
    pm2 = User.objects.create_user(username="elena_pm", email="elena@corp.com", password="password123", role=User.Role.PROJECT_MANAGER, first_name="Elena", last_name="Rose", specialization="Scrum")
    
    tm1 = User.objects.create_user(username="alex_tm", email="alex@corp.com", password="password123", role=User.Role.TEAM_MEMBER, first_name="Alex", last_name="Dev", skills="Python, React")
    tm2 = User.objects.create_user(username="jess_tm", email="jess@corp.com", password="password123", role=User.Role.TEAM_MEMBER, first_name="Jess", last_name="UI", skills="Figma, UI/UX")
    tm3 = User.objects.create_user(username="mark_tm", email="mark@corp.com", password="password123", role=User.Role.TEAM_MEMBER, first_name="Mark", last_name="Ops", skills="AWS, Docker")

    print("Creating Projects...")
    p1 = Project.objects.create(
        name="TaskVision Redesign",
        description="Overhaul the UI/UX for the main dashboard.",
        status="active",
        priority="high",
        budget=25000.00,
        start_date=timezone.now().date(),
        end_date=(timezone.now() + timedelta(days=60)).date(),
        assigned_to=pm1,
        created_by=po
    )
    p1.team_members.set([tm1, tm2])

    p2 = Project.objects.create(
        name="Backend Migration",
        description="Migrate Postgres DB to MySQL system.",
        status="completed",
        priority="high",
        budget=10500.00,
        start_date=(timezone.now() - timedelta(days=30)).date(),
        end_date=(timezone.now() - timedelta(days=5)).date(),
        assigned_to=pm2,
        created_by=po
    )
    p2.team_members.set([tm1, tm3])
    
    p3 = Project.objects.create(
        name="Analytics Dashboard",
        description="Add charting functionality for managers.",
        status="pending",
        priority="medium",
        start_date=(timezone.now() + timedelta(days=10)).date(),
        end_date=(timezone.now() + timedelta(days=40)).date(),
        assigned_to=pm1,
        created_by=po
    )
    p3.team_members.set([tm2, tm3])

    print("Creating Tasks...")
    Task.objects.create(project=p1, title="Design mockups", description="Create figma mockups for the new UI", status="completed", priority="high", due_date=timezone.now() + timedelta(days=2), assigned_to=tm2, created_by=pm1)
    Task.objects.create(project=p1, title="Frontend Implementation", description="Convert figma to HTML/CSS", status="in_progress", priority="medium", due_date=timezone.now() + timedelta(days=10), assigned_to=tm1, created_by=pm1)
    
    Task.objects.create(project=p2, title="Schema Design", description="Map out the tables", status="completed", priority="high", due_date=timezone.now() - timedelta(days=15), assigned_to=tm1, created_by=pm2)
    Task.objects.create(project=p2, title="Data Migration", description="Move data from dev to production", status="completed", priority="high", due_date=timezone.now() - timedelta(days=6), assigned_to=tm3, created_by=pm2)
    
    Task.objects.create(project=p3, title="Chart.js Integration", description="Start hooking up the endpoints to charts", status="todo", priority="medium", due_date=timezone.now() + timedelta(days=20), assigned_to=tm2, created_by=pm1)

    print("Creating Notifications...")
    Notification.objects.create(recipient=pm1, title="Help Requested", message="Alex needs help with Frontend Implementation.")
    Notification.objects.create(recipient=po, title="Project Completed", message="Backend Migration has been successfully wrapped up.")
    
    print("\n--- MOCK DATA GENERATED SUCCESSFULLY! ---")
    print("Test Logins (Password for all is 'password123'):")
    print("- Product Owner: sarah_po (or sarah@corp.com)")
    print("- Project Manager: david_pm (or david@corp.com)")
    print("- Team Member: alex_tm (or alex@corp.com)")

if __name__ == '__main__':
    seed_data()
