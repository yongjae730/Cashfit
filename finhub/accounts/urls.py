from django.urls import path,include
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.register_user, name='register_user'),
    path('profile/', views.user_profile, name='user_profile'),
]