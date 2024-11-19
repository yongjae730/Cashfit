from email.mime import audio
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomRegisterSerializer
from django.shortcuts import render
from rest_framework.decorators import api_view

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
