from django.urls import path
from .views import RegisterView, CustomAuthToken, UserProfileView, UserListView, GoogleLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('google/', GoogleLoginView.as_view(), name='google-login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users/', UserListView.as_view(), name='user-list'),
]

