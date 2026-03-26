from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Frontend pages
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('index.html', TemplateView.as_view(template_name='index.html')),
    path('login.html', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register.html', TemplateView.as_view(template_name='register.html'), name='register'),
    path('signup.html', TemplateView.as_view(template_name='register.html'), name='signup'),
    path('project-manager.html', TemplateView.as_view(template_name='project-manager.html'), name='pm_dashboard'),
    path('team-member.html', TemplateView.as_view(template_name='team-member.html'), name='tm_dashboard'),
    path('product-owner.html', TemplateView.as_view(template_name='product-owner.html'), name='po_dashboard'),
    
    # API Routes
    path('api/', include('core.urls')),
    path('api/auth/', include('accounts.urls')),
]

