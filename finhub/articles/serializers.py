from rest_framework import serializers
from .models import Article, ArticleComment
class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'create_at', 'update_at')


        
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('users',)

class ArticleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = ('id', 'content', 'users', 'create_at', 'is_deleted')

class ArticleDetailSerializer(serializers.ModelSerializer):
    comments = ArticleCommentSerializer(source='articlecomments', many=True)
    comments_count = serializers.IntegerField(source='articlecomments.count', read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'users', 'create_at', 'update_at', 'comments', 'comments_count')