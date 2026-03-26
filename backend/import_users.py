import os
import django  # type: ignore
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskvision.settings")
django.setup()

from django.contrib.auth import get_user_model  # type: ignore
from django.utils import timezone  # type: ignore

User = get_user_model()

# CSV Data directly embedded for the script
RAW_DATA = """UserID,FirstName,LastName,Email,Phone,Role,Department,Username,Password,CreatedAt
1,Arjun,Prakash,arjun.po@gmail.com,9876543210,Product Owner,Management,arjun_po,pass123,2024-01-10
2,Meena,Krishnan,meena.po@gmail.com,9876501234,Product Owner,Management,meena_po,pass123,2024-01-12
3,Rahul,Sharma,rahul.pm@gmail.com,9123456780,Product Manager,Product,rahul_pm,pass123,2024-02-01
4,Sneha,Iyer,sneha.pm@gmail.com,9988776655,Product Manager,Product,sneha_pm,pass123,2024-02-05
5,Karthik,Raj,karthik.tm@gmail.com,9345678901,Team Member,Development,karthik_tm,pass123,2024-03-01
6,Divya,Ravi,divya.tm@gmail.com,9789012345,Team Member,Development,divya_tm,pass123,2024-03-03
7,Ajay,Singh,ajay.tm@gmail.com,9871234560,Team Member,Testing,ajay_tm,pass123,2024-03-10
8,Neha,Gupta,neha.tm@gmail.com,9812345670,Team Member,Design,neha_tm,pass123,2024-03-15
9,Vikram,Verma,vikram.tm@gmail.com,9090909090,Team Member,Development,vikram_tm,pass123,2024-03-20
10,Priya,Nair,priya.tm@gmail.com,9012345678,Team Member,Testing,priya_tm,pass123,2024-03-25"""

def load_users():
    print("🚀 Starting User Import Process...")
    
    lines = RAW_DATA.strip().split('\n')
    lines.pop(0) # Skip header
    
    for line in lines:
        parts = line.split(',')
        if len(parts) != 10:
            continue
            
        user_id, first_name, last_name, email, phone, role_str, department, username, password, created_at = parts
        
        # Map Role String to DB Choice
        role_map = {
            'Product Owner': 'PO',
            'Product Manager': 'PM', # Mapping given Product Manager to Project Manager role PM
            'Team Member': 'TM'
        }
        db_role = role_map.get(role_str, 'TM')
        
        # We'll use Email as Username since the login form asks for Email
        # but technically we save both in DB
        
        print(f"Creating/Updating user: {first_name} {last_name} ({db_role})")
        
        # Prepare defaults based on role to store "Department" info
        defaults = {
            'email': email,
            'role': db_role,
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
        }
        
        if db_role == 'PO':
            defaults['industry'] = department
        elif db_role == 'PM':
            defaults['specialization'] = department
        elif db_role == 'TM':
            defaults['skills'] = department
            
        try:
            # Parse Date
            dt = datetime.strptime(created_at, "%Y-%m-%d")
            defaults['date_joined'] = timezone.make_aware(dt)
        except ValueError:
            pass
            
        # Create or update
        user, created = User.objects.update_or_create(
            username=email, # Using email as username for consistency with login
            defaults=defaults
        )
        
        # Ensure password is set (hashed)
        user.set_password('pass123') # explicitly using the pass123 from CSV
        user.save()
        
    print("\n✅ User Import Complete!")
    print("\nYou can now login with any of the imported emails and password 'pass123'.")

if __name__ == "__main__":
    load_users()
