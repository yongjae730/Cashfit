"""finhub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from accounts.views import register_user,user_profile,update_profile  # 커스텀 뷰 임포트

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/accounts/',include('accounts.urls')),
    path('api/financials/',include('financials.urls')),
    path('api/articles/',include('articles.urls')),
    path('chatbot/', include('chatbot.urls')),
    # 나중에 추가 할지말지
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/signup/', register_user, name='register_user'),
    path('accounts/user_profile/', user_profile, name='user_profile'),
    path('accounts/update/', update_profile, name='update_profile'),
    # path('accounts/signup/', include('dj_rest_auth.registration.urls')),
]
