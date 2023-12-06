from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, LogoutView, user_profile

urlpatterns = [
    path('register/', RegisterView.as_view(), name = 'register'), 
    path('login/', LoginView.as_view(), name = 'login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('administrate/profile/<str:email>', user_profile, name='administrate_profile' ),
]