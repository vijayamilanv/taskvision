import os
import django # type: ignore
import random
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskvision.settings")
django.setup()

from django.contrib.auth import get_user_model # type: ignore
from django.utils import timezone # type: ignore
from core.models import Project, Task, TaskComment, TaskActivity # type: ignore

User = get_user_model()

def seed_tm1_integration():
    print("🚀 Integrating tm1@taskvision.com with exact PO and PM projects...")
    
    # 1. Fetch exact demo accounts
    po_user = User.objects.filter(email='po@taskvision.com').first()
    pm_user = User.objects.filter(email='pm@taskvision.com').first()
    tm1_user = User.objects.filter(email='tm1@taskvision.com').first()
    
    if not all([po_user, pm_user, tm1_user]):
        print("❌ Error: Could not find exactly po, pm, or tm1 demo accounts. Did you run seed_data.py?")
        return

    # 2. Get the core projects managed by pm and owned by po
    # Let's just grab ALL projects where either PO is owner or PM is assigned manager.
    core_projects = Project.objects.filter(owner=po_user) | Project.objects.filter(assigned_to=pm_user)
    core_projects = core_projects.distinct()
    
    if core_projects.count() == 0:
        print("⚠️ No projects found for PO/PM. Creating a core integration project...")
        core_projects = [Project.objects.create(
            name="TaskVision NextGen Core",
            description="The core integration project between PO, PM, and TM1.",
            status="active",
            priority="high",
            budget=250000.00,
            start_date=timezone.now().date(),
            owner=po_user,
            assigned_to=pm_user
        )]
    
    print(f"🔗 Linking TM1 to {len(core_projects)} core projects established by PO/PM...")

    # 3. Add TM1 to all these projects
    for p in core_projects:
        p.team_members.add(tm1_user)
        print(f" - Added TM1 to project: {p.name}")

    # 4. Generate hyper-specific integration Tasks assigned to TM1 on these projects
    task_templates = [
        "Implement Backend API for {proj}",
        "Design Figma Views for {proj}",
        "Resolve Critical Bug in {proj}",
        "Refactor Auth Flow for {proj}",
        "Write Documentation for {proj}"
    ]

    print(f"📋 Generating direct task assignments for TM1...")
    
    for p in core_projects:
        for _ in range(3): # 3 exact tasks per shared project
            title_template = random.choice(task_templates)
            task = Task.objects.create(
                title=title_template.format(proj=p.name),
                description=f"Directly assigned by Project Manager ({pm_user.first_name}) via Product Owner ({po_user.first_name}) directive.",
                project=p,
                deadline=timezone.now() + timedelta(days=random.randint(1, 14)),
                priority=random.choice(['high', 'medium', 'low']),
                progress=random.randint(20, 90),
                status=random.choice(['todo', 'in_progress']),
                assigned_to=tm1_user
            )
            
            # Simulate collaborative Activity & Comments between PO, PM, and TM1
            TaskActivity.objects.create(
                task=task,
                user=pm_user,
                activity_type="Assigned",
                description=f"{pm_user.first_name} assigned this task to {tm1_user.first_name}."
            )
            TaskComment.objects.create(
                task=task,
                user=po_user,
                content=f"Please prioritize this, {tm1_user.first_name}. It's critical for our end-of-quarter milestone."
            )
            
    print(f"\n✅ Integration Complete! {len(core_projects) * 3} targeted tasks created for TM1.")
    print("Now if TM1 logs in, they will see tasks directly tied to PO's/PM's dashboards!")

if __name__ == '__main__':
    seed_tm1_integration()
