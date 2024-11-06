from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, PostView, AvatarView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserProfileView.as_view(), name='user-profile'),
    path('posts/', PostView.as_view(), name='posts'),
    path('avatar', AvatarView.as_view(), name='avatar')
]
