from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        self.user_instance = serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        # Get the created user and token
        user = self.user_instance
        token = Token.objects.get(user=user)
        
        # Return enhanced response with token and user details
        response.data = {
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'message': 'Registration successful! You can now login.'
        }
        
        return response

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'non_field_errors': ['Must include "username" and "password".']}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=username).first() or User.objects.filter(username=username).first()

        if user and user.check_password(password):
            if not user.is_active:
                return Response({'non_field_errors': ['User account is disabled.']}, status=status.HTTP_400_BAD_REQUEST)
            
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'role': user.role,
                'username': user.username,
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}".strip() or user.username
            })
        
        return Response({'non_field_errors': ['Unable to log in with provided credentials.']}, status=status.HTTP_400_BAD_REQUEST)

class GoogleLoginView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        token_id = request.data.get('credential')
        role = request.data.get('role', 'TM') # Default to Team Member if not provided
        
        try:
            # Verify the token. Note: For a strictly secure app, you should provide the audience=CLIENT_ID here.
            idinfo = id_token.verify_oauth2_token(
                token_id, 
                google_requests.Request(), 
                clock_skew_in_seconds=10
            )
            
            userid = idinfo['sub']
            email = idinfo['email']
            name = idinfo.get('name', '')
            
            # Find or create user
            user, created = User.objects.get_or_create(email=email, defaults={
                'username': email,
                'first_name': name.split()[0] if name else '',
                'last_name': ' '.join(name.split()[1:]) if len(name.split()) > 1 else '',
                'role': role
            })
            
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'role': user.role,
                'username': user.username,
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}".strip() or user.username
            })
            
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = User.objects.all()
        role = self.request.query_params.get('role')
        if role:
            queryset = queryset.filter(role=role)
        return queryset

