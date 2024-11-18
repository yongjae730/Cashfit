from rest_framework import serializers
from .models import Article, ArticleComment
class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content')


        
class ArticleSerializer(serializers.ModelSerializer):
    class CommentSerialzers(serializers.ModelSerializer):
        class Meta:
            model = ArticleComment
            fields = '__all__'
            read_only_fields = ('user',)
    articlecomments = CommentSerialzers(many=True, read_only=True)
    article_count = CommentSerialzers(source='articlecomments.count', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user',)

