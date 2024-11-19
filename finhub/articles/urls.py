from django.urls import path,include
from . import views
app_name = 'articles'
app_name = 'articles'

urlpatterns = [
    # 게시글 관련 URL
    path('', views.article_list, name='article_list'),  # 게시글 리스트 조회
    path('create/', views.article_create, name='article_create'),  # 게시글 생성
    path('<int:article_pk>/', views.article_detail, name='article_detail'),  # 게시글 상세 페이지 (댓글 포함)
    path('<int:article_pk>/update-delete/', views.article_update_delete, name='article_update_delete'),  # 게시글 수정/삭제

    # 댓글 관련 URL
    path('<int:article_pk>/comments/create/', views.create_comment, name='create_comment'),  # 댓글 생성
    path('<int:article_pk>/comments/<int:comment_pk>/update-delete/', views.comment_update_delete, name='comment_update_delete'),  # 댓글 수정/삭제
]