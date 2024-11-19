'''
게시판 기능인데 샘플코드라 주석 풀지말지 결정해야하고,
permission_classes 데코레이터로 권한 부여함 
''' 
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import ArticleCommentSerializer
from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import ArticleListSerializer, ArticleSerializer,ArticleDetailSerializer
from .models import Article, ArticleComment

# 게시글 리스트 조회 (권한 없음)
@api_view(['GET'])
@permission_classes([AllowAny])  # 누구나 접근 가능
def article_list(request):
    articles = get_list_or_404(Article)
    serializer = ArticleListSerializer(articles, many=True)
    return Response(serializer.data)

# 게시글 생성 (인증 필요)
@api_view(['POST'])
# @permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def article_create(request):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(users=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 게시글 상세보기
@api_view(['GET'])
@permission_classes([AllowAny])  # 누구나 접근 가능
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

# 게시글 수정/삭제
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def article_update_delete(request, article_pk):
    # 게시글 객체 가져오기 (작성자만 접근 가능)
    article = get_object_or_404(Article, pk=article_pk)

    # 작성자 확인
    if article.users != request.user:
        return Response({'message': '작성자만 수정/삭제할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':  # 수정
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':  # 삭제
        article.delete()
        return Response({'message': '게시글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)


# 댓글 생성
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 댓글 작성 가능
def create_comment(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = ArticleCommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(users=request.user, articles=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 댓글 수정/삭제
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_update_delete(request, article_pk, comment_pk):
    # 댓글 객체 가져오기 (작성자만 접근 가능)
    comment = get_object_or_404(ArticleComment, pk=comment_pk, articles__pk=article_pk)

    # 작성자 확인
    if comment.users != request.user:
        return Response({'message': '작성자만 수정/삭제할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':  # 수정
        serializer = ArticleCommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':  # 삭제
        comment.is_deleted = True
        comment.save()
        return Response({'message': '댓글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
