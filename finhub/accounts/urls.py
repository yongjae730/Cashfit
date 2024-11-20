from django.urls import path,include
from . import views


urlpatterns = [
    path('accounts/signup/', views.register_user, name='register_user'),
    path('profile/', views.user_profile, name='user_profile'),
]