from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ProjectViewSet, CommentViewSet, NotificationViewSet

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='project')
router.register('tasks', TaskViewSet, basename='task')
router.register('comments', CommentViewSet, basename='comment')
router.register('notifications', NotificationViewSet, basename='notification')

from .ai_views import AIChatView
from .views import DashboardAPIView

urlpatterns = [
    path('', include(router.urls)),
    path('ai/chat/', AIChatView.as_view(), name='ai_chat'),
    path('dashboard/', DashboardAPIView.as_view(), name='dashboard_api'),
]
