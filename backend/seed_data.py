import os
import django
from datetime import date, timedelta
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskvision.settings")
django.setup()

from django.contrib.auth import get_user_model
from core.models import Project, Task, TaskComment, TaskActivity

User = get_user_model()

def seed():
    print("Cleaning database...")
    # Be careful, this deletes everything mostly, so maybe just create if doesn't exist
    # Let's just create new items instead of deleting everything, just in case they have data.
    # Actually, a clean slate is usually preferred for dummy data, but if they have their own user, let's keep it.
    
    print("Creating users...")
    # Product Owner
    po, _ = User.objects.get_or_create(username='po_dummy', defaults={'email': 'po@example.com', 'role': 'PO', 'first_name': 'Alice', 'last_name': 'PO'})
    if getattr(po, 'password', '') == '':
        po.set_password('password123')
        po.save()

    # Project Managers
    pm1, _ = User.objects.get_or_create(username='pm_jordan', defaults={'email': 'jordan@example.com', 'role': 'PM', 'first_name': 'Jordan', 'last_name': 'PM'})
    if getattr(pm1, 'password', '') == '':
        pm1.set_password('password123')
        pm1.save()

    # Team Members
    tm1, _ = User.objects.get_or_create(username='tm_sam', defaults={'email': 'sam@example.com', 'role': 'TM', 'first_name': 'Sam', 'last_name': 'Dev'})
    tm2, _ = User.objects.get_or_create(username='tm_alex', defaults={'email': 'alex@example.com', 'role': 'TM', 'first_name': 'Alex', 'last_name': 'Designer'})
    tm3, _ = User.objects.get_or_create(username='tm_taylor', defaults={'email': 'taylor@example.com', 'role': 'TM', 'first_name': 'Taylor', 'last_name': 'QA'})
    
    for tm in [tm1, tm2, tm3]:
        if getattr(tm, 'password', '') == '':
            tm.set_password('password123')
            tm.save()

    print("Creating projects...")
    proj1, _ = Project.objects.get_or_create(
        name="TaskVision Redesign",
        defaults={
            'description': "Complete overhaul of the UI and implementing Jira-like features.",
            'start_date': date.today() - timedelta(days=10),
            'end_date': date.today() + timedelta(days=30),
            'budget': 50000.00,
            'status': 'active',
            'created_by': po,
            'assigned_to': pm1
        }
    )
    proj1.team_members.set([tm1, tm2, tm3])

    proj2, _ = Project.objects.get_or_create(
        name="Mobile App MVP",
        defaults={
            'description': "React Native app for TaskVision mobile clients.",
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=60),
            'budget': 75000.00,
            'status': 'pending',
            'created_by': po,
            'assigned_to': pm1
        }
    )
    proj2.team_members.set([tm1, tm2])

    print("Creating tasks...")
    # Epic
    epic1, created = Task.objects.get_or_create(
        title="Epic: Jira Board Integration",
        project=proj1,
        defaults={
            'description': "Implement drag and drop Kanban boards across the platform with issue types.",
            'assigned_to': tm1,
            'due_date': date.today() + timedelta(days=5),
            'priority': 'high',
            'status': 'in_progress',
            'issue_type': 'epic',
            'created_by': pm1
        }
    )

    # Stories
    story1, _ = Task.objects.get_or_create(
        title="Design Kanban UI",
        project=proj1,
        defaults={
            'description': "Create Figma mockups for the drag and drop columns.",
            'parent_task': epic1,
            'assigned_to': tm2,
            'due_date': date.today() - timedelta(days=1),
            'priority': 'medium',
            'status': 'completed',
            'issue_type': 'story',
            'created_by': pm1
        }
    )

    story2, _ = Task.objects.get_or_create(
        title="Develop Backend APIs for Boards",
        project=proj1,
        defaults={
            'description': "Create serializers and endpoints for updating task statuses.",
            'parent_task': epic1,
            'assigned_to': tm1,
            'due_date': date.today() + timedelta(days=2),
            'priority': 'high',
            'status': 'in_progress',
            'issue_type': 'story',
            'created_by': pm1
        }
    )

    # Bugs
    bug1, _ = Task.objects.get_or_create(
        title="Drag Events Firing Twice",
        project=proj1,
        defaults={
            'description': "When releasing a card, the API call is duplicated.",
            'parent_task': story2,
            'assigned_to': tm3,
            'due_date': date.today() + timedelta(days=1),
            'priority': 'high',
            'status': 'todo',
            'issue_type': 'bug',
            'created_by': tm2
        }
    )

    # Normal Tasks
    task1, _ = Task.objects.get_or_create(
        title="Setup Mobile Repo",
        project=proj2,
        defaults={
            'description': "Initialize Expo/React Native repo for the new app.",
            'assigned_to': tm1,
            'due_date': date.today() + timedelta(days=5),
            'priority': 'medium',
            'status': 'todo',
            'issue_type': 'task',
            'created_by': pm1
        }
    )

    # Subtasks
    subtask1, _ = Task.objects.get_or_create(
        title="Configure ESLint",
        project=proj2,
        defaults={
            'description': "Add prettier and strict TS rules.",
            'parent_task': task1,
            'assigned_to': tm1,
            'due_date': date.today() + timedelta(days=3),
            'priority': 'low',
            'status': 'todo',
            'issue_type': 'subtask',
            'created_by': tm1
        }
    )

    print("Adding Comments and Activity...")
    # Add activity & comments if none exist
    if not TaskComment.objects.filter(task=epic1).exists():
        TaskActivity.objects.create(task=epic1, user=pm1, action="Created task")
        
        c1 = TaskComment.objects.create(task=epic1, author=pm1, content="Let's make sure we study Atlassian's drag and drop carefully before starting.")
        c1.created_at = date.today() - timedelta(days=2)
        c1.save()

        TaskActivity.objects.create(task=epic1, user=tm1, action="Updated fields", details="Updated status to In Progress")
        
        c2 = TaskComment.objects.create(task=epic1, author=tm1, content="Backend structures are mostly ready, moving onto the frontend JS.")
        c2.created_at = date.today() - timedelta(days=1)
        c2.save()

        c3 = TaskComment.objects.create(task=epic1, author=tm2, content="UI is done! See attachments folder. Waiting on API to wire it up.")
        c3.created_at = date.today()
        c3.save()

    if not TaskComment.objects.filter(task=bug1).exists():
        TaskActivity.objects.create(task=bug1, user=tm2, action="Created task")
        TaskActivity.objects.create(task=bug1, user=pm1, action="Updated fields", details="Assigned task to tm_taylor")
        
        c4 = TaskComment.objects.create(task=bug1, author=tm3, content="I'll look into the drag events. Looks like bubbling might be unchecked.")
        c4.save()


    print("Dummy data generation complete!")
    print("-----------------------------------------------------")
    print("Try logging into the dashboard using one of these accounts:")
    print("Project Manager -> Username: pm_jordan | Password: password123")
    print("Team Member     -> Username: tm_sam    | Password: password123")
    print("-----------------------------------------------------")

if __name__ == "__main__":
    seed()
