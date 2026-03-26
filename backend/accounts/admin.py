from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role', 'phone', 'company', 'industry', 'specialization', 'years_experience', 'skills', 'experience_level', 'reports_to')}),
    )

admin.site.register(User, CustomUserAdmin)
