from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        PRODUCT_OWNER = 'PO', 'Product Owner'
        PROJECT_MANAGER = 'PM', 'Project Manager'
        TEAM_MEMBER = 'TM', 'Team Member'
        ADMIN = 'ADMIN', 'Admin'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.TEAM_MEMBER)
    phone = models.CharField(max_length=20, blank=True)
    
    # PO Fields
    company = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    
    # PM Fields
    specialization = models.CharField(max_length=100, blank=True)
    years_experience = models.IntegerField(default=0, blank=True, null=True)
    
    # TM Fields
    skills = models.TextField(blank=True) # Comma separated
    experience_level = models.CharField(max_length=50, blank=True)
    reports_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='team_members')

    # Gamification & AI Analytics
    points = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    last_active_date = models.DateField(null=True, blank=True)
    productivity_score = models.FloatField(default=0.0) # Evaluated out of 100

    def __str__(self):
        return f"{self.username} ({self.role})"
