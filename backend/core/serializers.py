from rest_framework import serializers  # pyre-ignore
from .models import Task, Project, TaskComment, TaskActivity, Notification  # pyre-ignore

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class TaskCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = TaskComment
        fields = '__all__'

class TaskActivitySerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = TaskActivity
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.username')
    assigned_to_details = serializers.SerializerMethodField()
    team_members_details = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'status', 'priority', 'budget', 
            'start_date', 'created_at', 'owner', 'owner_name', 
            'assigned_to', 'assigned_to_details', 
            'team_members', 'team_members_details'
        ]
        read_only_fields = ['owner']

    def get_assigned_to_details(self, obj):
        if obj.assigned_to:
            return {
                'id': obj.assigned_to.id,
                'username': obj.assigned_to.username,
                'name': f"{obj.assigned_to.first_name} {obj.assigned_to.last_name}"
            }
        return None

    def get_team_members_details(self, obj):
        return [{
            'id': user.id,
            'username': user.username,
            'name': f"{user.first_name} {user.last_name}"
        } for user in obj.team_members.all()]

class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.ReadOnlyField(source='project.name')
    assigned_to_name = serializers.ReadOnlyField(source='assigned_to.username')
    assigned_to_details = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'project', 'project_name', 
            'deadline', 'priority', 'progress', 'status', 
            'assigned_to', 'assigned_to_name', 'assigned_to_details', 'created_at'
        ]

    def get_assigned_to_details(self, obj):
        if obj.assigned_to:
            return {
                'id': obj.assigned_to.id,
                'username': obj.assigned_to.username,
                'name': f"{obj.assigned_to.first_name} {obj.assigned_to.last_name}"
            }
        return None
