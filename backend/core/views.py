from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task, Project, TaskComment, TaskActivity, Notification
from django.db.models import Count
from django.contrib.auth import get_user_model

User = get_user_model()
from .serializers import (
    TaskSerializer, ProjectSerializer, 
    TaskCommentSerializer, TaskActivitySerializer, 
    NotificationSerializer
)

class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', 'TM')
        if role in ['PO', 'Product Owner']:
            return Project.objects.all()  # PO sees all
        elif role in ['PM', 'Project Manager']:
            return Project.objects.filter(assigned_to=user) # PM sees managed
        else:
            return Project.objects.filter(team_members=user) # TM sees assigned

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', 'TM')
        if role in ['PO', 'Product Owner']:
            return Task.objects.filter(project__owner=user)
        elif role in ['PM', 'Project Manager']:
            return Task.objects.filter(project__assigned_to=user)
        return Task.objects.filter(assigned_to=user)

class CommentViewSet(ModelViewSet):
    serializer_class = TaskCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TaskComment.objects.filter(task__user=self.request.user) | \
               TaskComment.objects.filter(task__project__owner=self.request.user) | \
               TaskComment.objects.filter(task__project__assigned_to=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role = getattr(user, 'role', 'TM')
        
        # Base Queryset based on role
        if role in ['PO', 'Product Owner']:
            projects = Project.objects.all()
        elif role in ['PM', 'Project Manager']:
            projects = Project.objects.filter(assigned_to=user)
        else:
            projects = Project.objects.filter(team_members=user)

        total_users = User.objects.count()
        total_projects = projects.count()
        completed_projects = projects.filter(status='completed').count()
        in_progress_projects = projects.filter(status='active').count()

        status_distribution = list(projects.values('status').annotate(count=Count('id')))
        priority_distribution = list(projects.values('priority').annotate(count=Count('id')))
        
        recent_projects = projects.order_by('-created_at')[:5]

        return Response({
            'totalUsers': total_users,
            'totalProjects': total_projects,
            'completedProjects': completed_projects,
            'inProgressProjects': in_progress_projects,
            'projectsByStatus': status_distribution,
            'projectsByPriority': priority_distribution,
            'recentProjects': ProjectSerializer(recent_projects, many=True).data
        })
