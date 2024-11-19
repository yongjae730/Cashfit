from django.urls import path,include
from . import views
app_name = 'articles'
urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('<int:article_pk>/', views.article_detail, name='article_detail'),
    path('<int:article_pk>/comments/', views.list_comments, name='list_comments'),
    path('<int:article_pk>/comments/create/', views.create_comment, name='create_comment'),
]