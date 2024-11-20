from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.response import Response
from articles.models import Article  
from financials.models import FinancialProductLike, FinancialComment
from .serializers import CustomRegisterSerializer
from financials.serializers import FinancialProductsSerializer, FinancialCommentSerializer
from articles.serializers import ArticleSerializer
from .serializers import UserUpdateSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions



User = get_user_model()
@api_view(['POST'])
def register_user(request):
    """
    회원가입 데이터를 처리하고 저장하는 뷰
    """
    serializer = CustomRegisterSerializer(data=request.data)
    if serializer.is_valid():
        # 유저 저장
        user = serializer.save(request)
        
        # 저장된 데이터를 가공하여 반환
        saved_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "nickname": user.nickname,
            "age": user.age,
            "capital": user.capital,
            "sido": user.sido,
            "sigungus": user.sigungus,
        }
        # 추가 작업 (예: 로깅, 외부 API 호출 등)
        print("New user created:", saved_data)
    
        return Response(saved_data, status=status.HTTP_201_CREATED)
    if not serializer.is_valid():
        print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@login_required
def user_profile(request):
    user = request.user

    # 기본 유저 정보
    user_info = {
        "username": user.username,
        "nickname": user.nickname,
        "age": user.age,
        "capital": user.capital,
        "sido": user.sido,
        "sigungus": user.sigungus,
    }

    # 좋아요 한 금융 상품
    liked_products = FinancialProductLike.objects.filter(user=user)
    liked_products_data = FinancialProductsSerializer(
        [like.product for like in liked_products], many=True
    ).data

    # 작성한 댓글
    comments = FinancialComment.objects.filter(users=user)
    comments_data = FinancialCommentSerializer(comments, many=True).data

    # 작성한 글
    articles = Article.objects.filter(users_id=user)
    articles_data = ArticleSerializer(articles, many=True).data

    # 최종 응답 데이터
    profile_data = {
        "user_info": user_info,
        "liked_products": liked_products_data,
        "comments": comments_data,
        "articles": articles_data,
    }

    return Response(profile_data)


@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = UserUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

