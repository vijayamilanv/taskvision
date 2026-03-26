import os
import django
from datetime import datetime
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskvision.settings")
django.setup()

from django.contrib.auth import get_user_model
from core.models import Project

User = get_user_model()

RAW_DATA = """ProjectID,ProjectName,Description,StartDate,EndDate,Status,Owner,Priority,Budget
1,Project Alpha,Web app for task management,2024-01-01,2024-03-30,Completed,Arjun,High,50000
2,Project Beta,E-commerce platform,2024-01-10,2024-05-15,In Progress,Meena,High,120000
3,Project Gamma,Mobile banking app,2024-02-01,2024-06-20,In Progress,Rahul,Critical,200000
4,Project Delta,AI chatbot system,2024-02-15,2024-04-30,Completed,Sneha,Medium,80000
5,Project Epsilon,Inventory system,2024-03-01,2024-07-01,Not Started,Karthik,Medium,60000
6,Project Zeta,Online learning platform,2024-03-10,2024-08-10,In Progress,Divya,High,150000
7,Project Eta,Healthcare app,2024-04-01,2024-09-01,Not Started,Ajay,Critical,180000
8,Project Theta,Travel booking system,2024-04-15,2024-07-30,In Progress,Neha,High,100000
9,Project Iota,Social media app,2024-05-01,2024-10-01,In Progress,Vikram,High,130000
10,Project Kappa,Food delivery app,2024-05-10,2024-09-20,Not Started,Priya,Medium,90000
11,Project Lambda,CRM software,2024-06-01,2024-12-01,In Progress,Arjun,High,140000
12,Project Mu,HR management system,2024-06-10,2024-11-10,Completed,Meena,Medium,70000
13,Project Nu,Online exam portal,2024-07-01,2024-12-15,In Progress,Rahul,High,110000
14,Project Xi,IoT smart home system,2024-07-15,2025-01-15,Not Started,Sneha,Critical,210000
15,Project Omicron,Warehouse system,2024-08-01,2024-12-01,In Progress,Karthik,Medium,85000
16,Project Pi,Video streaming app,2024-08-10,2025-02-10,Not Started,Divya,High,170000
17,Project Rho,Online voting system,2024-09-01,2025-01-01,In Progress,Ajay,Critical,160000
18,Project Sigma,Taxi booking app,2024-09-10,2025-03-10,Not Started,Neha,High,140000
19,Project Tau,Fitness tracking app,2024-10-01,2025-02-01,In Progress,Vikram,Medium,75000
20,Project Upsilon,Event management system,2024-10-10,2025-04-10,Not Started,Priya,Medium,65000
21,Project Phi,Job portal,2024-11-01,2025-05-01,In Progress,Arjun,High,120000
22,Project Chi,Online auction system,2024-11-10,2025-03-10,Completed,Meena,Medium,80000
23,Project Psi,Cloud storage system,2024-12-01,2025-06-01,In Progress,Rahul,High,190000
24,Project Omega,Cybersecurity tool,2024-12-10,2025-07-10,Not Started,Sneha,Critical,220000
25,Project Nova,AI recommendation engine,2024-01-20,2024-06-20,Completed,Karthik,High,160000
26,Project Orion,Music streaming app,2024-02-20,2024-08-20,In Progress,Divya,Medium,90000
27,Project Vega,Online marketplace,2024-03-20,2024-09-20,In Progress,Ajay,High,140000
28,Project Atlas,Project management tool,2024-04-20,2024-10-20,Not Started,Neha,High,130000
29,Project Apollo,Space data analysis,2024-05-20,2025-01-20,In Progress,Vikram,Critical,250000
30,Project Titan,Big data analytics system,2024-06-20,2025-02-20,Not Started,Priya,Critical,240000
31,Project Phoenix,Disaster recovery system,2024-07-20,2025-03-20,In Progress,Arjun,High,180000
32,Project Zenith,Stock trading app,2024-08-20,2025-04-20,Not Started,Meena,High,200000
33,Project Horizon,Weather prediction system,2024-09-20,2025-05-20,In Progress,Rahul,Medium,95000
34,Project Pulse,Health monitoring system,2024-10-20,2025-06-20,Not Started,Sneha,High,120000
35,Project Spark,Startup management app,2024-11-20,2025-07-20,In Progress,Karthik,Medium,85000
36,Project Fusion,Energy management system,2024-12-20,2025-08-20,Not Started,Divya,High,175000
37,Project Edge,AI image recognition,2024-01-25,2024-07-25,Completed,Ajay,Critical,210000
38,Project Core,Backend API system,2024-02-25,2024-08-25,In Progress,Neha,Medium,70000
39,Project Nexus,Blockchain platform,2024-03-25,2024-09-25,Not Started,Vikram,Critical,230000
40,Project Orbit,Satellite tracking system,2024-04-25,2025-01-25,In Progress,Priya,High,190000
41,Project Quantum,Quantum computing simulation,2024-05-25,2025-02-25,Not Started,Arjun,Critical,300000
42,Project Matrix,Data visualization tool,2024-06-25,2025-03-25,In Progress,Meena,Medium,95000
43,Project Vector,Graphics design tool,2024-07-25,2025-04-25,Not Started,Rahul,Medium,85000
44,Project Prism,AR/VR application,2024-08-25,2025-05-25,In Progress,Sneha,High,200000
45,Project PulseX,Advanced health AI,2024-09-25,2025-06-25,Not Started,Karthik,Critical,220000
46,Project Aero,Drone control system,2024-10-25,2025-07-25,In Progress,Divya,High,180000
47,Project Terra,Smart agriculture system,2024-11-25,2025-08-25,Not Started,Ajay,Medium,100000
48,Project Aqua,Water monitoring system,2024-12-25,2025-09-25,In Progress,Neha,Medium,90000
49,Project Solar,Renewable energy tracker,2024-01-30,2024-07-30,Completed,Vikram,High,120000
50,Project Lunar,Moon mission analytics,2024-02-28,2024-08-28,In Progress,Priya,Critical,260000"""

def load_projects():
    print("🚀 Starting Project Import Process...")
    
    # Pre-fetch all users to map by First Name
    users_by_first_name = {user.first_name: user for user in User.objects.all() if user.first_name}
    
    status_map = {
        'Not Started': 'pending',
        'In Progress': 'active',
        'Completed': 'completed'
    }
    
    lines = RAW_DATA.strip().split('\n')[1:] # Skip header
    
    success_count = 0
    error_count = 0
    
    for line in lines:
        parts = line.split(',')
        if len(parts) != 9:
            continue
            
        project_id, name, desc, start_date_str, end_date_str, status_str, owner_name, priority, budget = parts
        
        # Map Status
        db_status = status_map.get(status_str, 'pending')
        
        # We lowercase priority to match DB choices ('high', 'medium', 'low', 'critical')
        db_priority = priority.lower()
        if db_priority == 'critical':
             db_priority = 'high' # critical is not in Project PRIORITY_CHOICES currently, only Task has priorites, but Project has 'low', 'medium', 'high' normally. We'll map Critical to High since Project only has Default="medium", though it is a charfield

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        except ValueError:
            start_date = None
            
        # Find Owner
        owner_user = users_by_first_name.get(owner_name)
        if not owner_user:
            print(f"⚠️ Warning: Could not find user with first name '{owner_name}'. Skipping project '{name}'.")
            error_count += 1
            continue
            
        print(f"Creating project: {name} (Owned by {owner_name})")
        
        try:
            # We'll set the owner and assigned_to to the same user for simplicity, or we can just set owner
            # For the dashboard logic: PO sees all, PM sees managed (assigned_to), TM sees assigned (team_members)
            
            project, created = Project.objects.update_or_create(
                name=name,
                defaults={
                    'description': desc,
                    'status': db_status,
                    'priority': db_priority,
                    'budget': Decimal(budget),
                    'start_date': start_date,
                    'owner': owner_user,
                    # We will set assigned_to if they are a PM, otherwise it stays null. 
                    # If they are TM, we add them to team_members
                    'assigned_to': owner_user if owner_user.role == 'PM' else None
                }
            )
            
            if owner_user.role == 'TM':
                project.team_members.add(owner_user)
                
            success_count += 1
        except Exception as e:
            print(f"❌ Error creating project {name}: {e}")
            error_count += 1
            
    print(f"\n✅ Project Import Complete! Successfully imported {success_count} projects. ({error_count} errors)")

if __name__ == "__main__":
    load_projects()
