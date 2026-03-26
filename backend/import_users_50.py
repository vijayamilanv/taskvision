import os
import django # type: ignore
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskvision.settings")
django.setup()

from django.contrib.auth import get_user_model # type: ignore
from django.utils import timezone # type: ignore

User = get_user_model()

# Parsed from the provided screenshot
names = [
    ("Vikram", "Iyer"), ("Meena", "Singh"), ("Arjun", "Prakash"), ("Meena", "Sharma"), ("Meena", "Prakash"),
    ("Ajay", "Nair"), ("Sneha", "Iyer"), ("Karthik", "Nair"), ("Meena", "Iyer"), ("Divya", "Gupta"),
    ("Karthik", "Raj"), ("Karthik", "Nair"), ("Sneha", "Singh"), ("Rahul", "Verma"), ("Sneha", "Singh"),
    ("Priya", "Singh"), ("Divya", "Ravi"), ("Ajay", "Nair"), ("Vikram", "Singh"), ("Arjun", "Ravi"),
    ("Arjun", "Verma"), ("Karthik", "Raj"), ("Divya", "Gupta"), ("Meena", "Prakash"), ("Karthik", "Gupta"),
    ("Vikram", "Verma"), ("Ajay", "Ravi"), ("Meena", "Verma"), ("Priya", "Raj"), ("Vikram", "Raj"),
    ("Neha", "Ravi"), ("Rahul", "Ravi"), ("Karthik", "Verma"), ("Vikram", "Nair"), ("Rahul", "Sharma"),
    ("Ajay", "Raj"), ("Rahul", "Kumar"), ("Divya", "Kumar"), ("Neha", "Kumar"), ("Karthik", "Sharma"),
    ("Karthik", "Singh"), ("Sneha", "Gupta"), ("Ajay", "Ravi"), ("Rahul", "Verma"), ("Neha", "Singh"),
    ("Arjun", "Gupta"), ("Priya", "Verma"), ("Priya", "Ravi"), ("Neha", "Gupta"), ("Divya", "Verma")
]

roles_abbr = [
    "PO", "PM", "TM", "PM", "TM", "PO", "TM", "PO", "TM", "PO",
    "PO", "PM", "PO", "PM", "TM", "PM", "PM", "PO", "PM", "PM",
    "PM", "PO", "PM", "PO", "PO", "PO", "PM", "PO", "PO", "TM",
    "PO", "TM", "TM", "PO", "PM", "TM", "PO", "TM", "TM", "PO",
    "PO", "PO", "PO", "PO", "TM", "TM", "PO", "TM", "PM", "TM"
]

dept_map = {
    "PO": "Management",
    "PM": "Product",
    "TM": "Development" # We'll cycle Dev, Testing, Design for TMs
}
tm_deps = ["Testing", "Development", "Design"]
tm_idx = 0

dates = [
    "2024-06-14", "2024-12-15", "2024-09-03", "2024-10-10", "2024-12-20",
    "2024-06-24", "2024-03-26", "2024-10-07", "2024-05-23", "2024-01-04",
    "2024-08-04", "2024-03-27", "2024-09-01", "2024-11-28", "2024-06-11",
    "2024-08-01", "2024-10-17", "2024-12-08", "2024-09-14", "2024-11-03",
    "2024-02-15", "2024-10-11", "2024-09-10", "2024-06-14", "2024-08-15",
    "2024-05-16", "2024-04-01", "2024-09-16", "2024-11-08", "2024-01-23",
    "2024-10-16", "2024-05-27", "2024-01-15", "2024-03-25", "2024-05-25",
    "2024-06-27", "2024-03-15", "2024-03-20", "2024-01-03", "2024-09-18",
    "2024-04-12", "2024-02-11", "2024-01-25", "2024-01-06", "2024-01-10",
    "2024-03-15", "2024-04-12", "2024-11-24", "2024-03-21", "2024-06-21"
]

def load_users():
    print("🚀 Starting User Import Process for 50 exact users...")
    
    for i in range(50):
        first, last = names[i]
        db_role = roles_abbr[i]
        
        # Determine exact department
        if db_role == "TM":
            global tm_idx
            dept = tm_deps[tm_idx % 3]
            tm_idx += 1
        else:
            dept = dept_map[db_role]
            
        # Emails format shown: vikram.iyer1@taskvision.com
        if i == 0:
            email = f"{first.lower()}.{last.lower()}@taskvision.com"
        else:
            email = f"{first.lower()}.{last.lower()}{i+1}@taskvision.com"
            
        username = f"{first.lower()}_{i+1}"
        password = "pass123"
        created_at = dates[i]
        phone = f"9{str(i+1).zfill(2)}1234567" # Dummy phone

        print(f"[{i+1}/50] Creating user: {first} {last} ({db_role}) - {email}")
        
        defaults = {
            'email': email,
            'role': db_role,
            'first_name': first,
            'last_name': last,
            'phone': phone,
        }
        
        if db_role == 'PO':
            defaults['industry'] = dept
        elif db_role == 'PM':
            defaults['specialization'] = dept
        elif db_role == 'TM':
            defaults['skills'] = dept
            
        try:
            dt = datetime.strptime(created_at, "%Y-%m-%d")
            defaults['date_joined'] = timezone.make_aware(dt)
        except ValueError:
            pass
            
        # Use email as the database username to align perfectly with custom auth fix
        user, created = User.objects.update_or_create(
            username=username, # The user explicitly has a username column! Let's save it. Wait, the login uses filter(username=username) OR filter(email=username). So we can safely save the requested username: vikram_1.
            defaults=defaults
        )
        
        user.set_password(password)
        user.save()
        
    print("\n✅ 50 Users Imported Successfully!")

if __name__ == "__main__":
    load_users()
