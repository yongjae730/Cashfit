from django.urls import path,include
from .views import register_user

urlpatterns = [
    path('accounts/signup/', register_user, name='register_user'),
]