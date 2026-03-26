import os
import django
from datetime import datetime, timedelta
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskvision.settings")
django.setup()

from django.contrib.auth import get_user_model
from core.models import Project, Task, TaskComment, TaskActivity, Notification

User = get_user_model()

def seed():
    print("🚀 Starting Seeding Process...")

    # --- 1. Create Users ---
    print("👥 Creating Users...")
    
    # Product Owner
    po, _ = User.objects.get_or_create(
        username='po@taskvision.com', 
        defaults={
            'email': 'po@taskvision.com',
            'role': 'PO',
            'first_name': 'Sarah',
            'last_name': 'Owner',
            'company': 'Visionary Tech',
            'industry': 'Software'
        }
    )
    po.set_password('password123')
    po.save()

    # Project Manager
    pm, _ = User.objects.get_or_create(
        username='pm@taskvision.com', 
        defaults={
            'email': 'pm@taskvision.com',
            'role': 'PM',
            'first_name': 'Mark',
            'last_name': 'Manager',
            'specialization': 'Agile Development',
            'years_experience': 8
        }
    )
    pm.set_password('password123')
    pm.save()

    # Team Members
    tm1, _ = User.objects.get_or_create(
        username='tm1@taskvision.com', 
        defaults={
            'email': 'tm1@taskvision.com',
            'role': 'TM',
            'first_name': 'Alex',
            'last_name': 'Dev',
            'skills': 'Python, Django, React',
            'experience_level': 'Senior',
            'reports_to': pm
        }
    )
    tm1.set_password('password123')
    tm1.save()

    tm2, _ = User.objects.get_or_create(
        username='tm2@taskvision.com', 
        defaults={
            'email': 'tm2@taskvision.com',
            'role': 'TM',
            'first_name': 'Jamie',
            'last_name': 'Coder',
            'skills': 'CSS, HTML, JavaScript',
            'experience_level': 'Junior',
            'reports_to': pm
        }
    )
    tm2.set_password('password123')
    tm2.save()

    # --- 2. Create Projects ---
    print("📁 Creating Projects...")
    
    proj1, _ = Project.objects.get_or_create(
        name="Enterprise Dashboard",
        defaults={
            'description': "A comprehensive dashboard for enterprise data visualization.",
            'owner': po,
            'assigned_to': pm,
            'status': 'active',
            'priority': 'high',
            'budget': 120000.00,
            'start_date': timezone.now().date() - timedelta(days=5)
        }
    )
    proj1.team_members.set([tm1, tm2])

    proj2, _ = Project.objects.get_or_create(
        name="AI Integration Module",
        defaults={
            'description': "Adding AI capabilities to our core processing engine.",
            'owner': po,
            'assigned_to': pm,
            'status': 'pending',
            'priority': 'medium',
            'budget': 85000.00,
            'start_date': timezone.now().date() + timedelta(days=10)
        }
    )
    proj2.team_members.set([tm1])

    # --- 3. Create Tasks ---
    print("📋 Creating Tasks...")
    
    # Project 1 Tasks
    t1, _ = Task.objects.get_or_create(
        title="Setup Base Architecture",
        project=proj1,
        defaults={
            'description': "Initialize the Django project structure and core configurations.",
            'deadline': timezone.now() + timedelta(days=2),
            'status': 'in_progress',
            'assigned_to': tm1,
            'progress': 30
        }
    )

    t2, _ = Task.objects.get_or_create(
        title="Design UI Components",
        project=proj1,
        defaults={
            'description': "Create reusable UI components using React and Tailwind.",
            'deadline': timezone.now() + timedelta(days=4),
            'status': 'todo',
            'assigned_to': tm2,
            'progress': 0
        }
    )

    t3, _ = Task.objects.get_or_create(
        title="API Documentation",
        project=proj1,
        defaults={
            'description': "Draft initial API documentation for internal use.",
            'deadline': timezone.now() - timedelta(days=1),
            'status': 'done',
            'assigned_to': tm1,
            'progress': 100
        }
    )

    # --- 4. Create Comments & Activities ---
    print("💬 Adding Comments & Activities...")
    
    TaskComment.objects.create(
        task=t1,
        user=pm,
        content="Great start on the architecture! Make sure to keep it modular."
    )

    TaskComment.objects.create(
        task=t1,
        user=tm1,
        content="Thanks, Mark. I'm focusing on the service layer right now."
    )

    TaskActivity.objects.create(
        task=t1,
        user=tm1,
        activity_type="Status Update",
        description="Changed status from 'todo' to 'in_progress'"
    )

    # --- 5. Create Notifications ---
    print("🔔 Sending Notifications...")
    
    Notification.objects.create(
        user=pm,
        title="New Task Created",
        message=f"A new task '{t1.title}' has been started by {tm1.first_name}."
    )

    Notification.objects.create(
        user=tm1,
        title="New Project Assigned",
        message=f"You have been added to the project: {proj1.name}"
    )

    print("\n✅ Seeding Complete!")
    print("\n--- Account Credentials ---")
    print(f"Product Owner:   email: po@taskvision.com   | password: password123")
    print(f"Project Manager: email: pm@taskvision.com   | password: password123")
    print(f"Team Member 1:   email: tm1@taskvision.com  | password: password123")
    print(f"Team Member 2:   email: tm2@taskvision.com  | password: password123")
    print("----------------------------\n")

if __name__ == "__main__":
    seed()
