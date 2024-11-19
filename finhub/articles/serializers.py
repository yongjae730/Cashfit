from os import read
from rest_framework import serializers
from .models import Article, ArticleComment
class ArticleListSerializer(serializers.ModelSerializer):
    users = serializers.StringRelatedField()
    class Meta:
        model = Article
        fields = ('id', 'title', 'content','create_at', 'update_at', 'users')


        
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('users',)

class ArticleCommentSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source="users.nickname", read_only=True)
    class Meta:
        model = ArticleComment
        fields = ('id', 'content', 'users', 'nickname','create_at', 'is_deleted')
        read_only_fields = ('users',"articles","create_at")

class ArticleDetailSerializer(serializers.ModelSerializer):
    comments = ArticleCommentSerializer(source='articlecomments', many=True)
    comments_count = serializers.IntegerField(source='articlecomments.count', read_only=True)
    nickname = serializers.CharField(source="users.nickname", read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'users', 'create_at', 'update_at', 'nickname', 'comments', 'comments_count')