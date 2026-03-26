import os
import django # type: ignore
import random
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskvision.settings")
django.setup()

from django.contrib.auth import get_user_model # type: ignore
from django.utils import timezone # type: ignore
from core.models import Project, Task # type: ignore

User = get_user_model()

def seed_team_member_data():
    print("🚀 Seeding dummy Projects and Tasks for Team Members...")
    
    # 1. Ensure we have at least one PO and PM to own/manage the projects
    po_user = User.objects.filter(role='PO').first()
    pm_user = User.objects.filter(role='PM').first()
    
    if not po_user or not pm_user:
        print("❌ Error: Need at least one PO and one PM in the database.")
        return

    # Get all Team Members
    team_members = User.objects.filter(role='TM')
    print(f"Found {team_members.count()} Team Members.")

    task_titles = [
        "Design Homepage Mockups", "Develop Authentication API",
        "Write Unit Tests for Core", "Optimize Database Queries",
        "Setup CI/CD Pipeline", "Create User Persona Docs",
        "Fix Navigation Bug #42", "Update Documentation",
        "Refactor Payment Gateway", "Implement WebSockets for Chat",
        "Conduct User Interviews", "Design Logo variations",
        "Debug Memory Leak", "Upgrade React Version",
        "Configure AWS S3 Buckets", "Translate App to Spanish",
        "Write Marketing Copy", "Analyze Competitor Features"
    ]

    project_titles = [
        "Project Alpha Rebrand", "Omega Server Migration",
        "Delta Mobile App", "Gamma Analytics Dashboard",
        "Zeta E-commerce Rewrite"
    ]

    # Create matching core projects
    projects = []
    for title in project_titles:
        proj, created = Project.objects.get_or_create(
            name=title,
            defaults={
                'description': f"A major initiative for {title}.",
                'status': random.choice(['active', 'pending', 'completed']),
                'priority': random.choice(['low', 'medium', 'high']),
                'budget': random.randint(10000, 150000),
                'start_date': timezone.now().date() - timedelta(days=random.randint(5, 60)),
                'owner': po_user,
                'assigned_to': pm_user
            }
        )
        projects.append(proj)

    # Seed data for each Team Member
    for tm in team_members:
        # Add TM to 1-3 random projects
        tm_projects = random.sample(projects, random.randint(1, 3))
        for p in tm_projects:
            p.team_members.add(tm)
            
        # Create 4-8 tasks for this TM
        num_tasks = random.randint(4, 8)
        for i in range(num_tasks):
            p = random.choice(tm_projects)
            Task.objects.create(
                title=f"{random.choice(task_titles)} ({tm.first_name})",
                description=f"Task assigned specifically to {tm.first_name} {tm.last_name}.",
                project=p,
                deadline=timezone.now() + timedelta(days=random.randint(1, 45)),
                priority=random.choice(['low', 'medium', 'high']),
                progress=random.randint(0, 100),
                status=random.choice(['todo', 'in_progress', 'done']),
                assigned_to=tm
            )
            
    print("\n✅ Successfully generated Dummy Projects and Tasks for all Team Members!")

if __name__ == '__main__':
    seed_team_member_data()
