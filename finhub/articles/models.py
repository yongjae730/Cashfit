from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()
class Article(models.Model):
    users = models.ForeignKey(User, on_delete = models.CASCADE, related_name='articles')
    title = models.CharField(max_length=255)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class ArticleComment(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_comments')
    articles = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='articlecomments')
    content = models.CharField(max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

