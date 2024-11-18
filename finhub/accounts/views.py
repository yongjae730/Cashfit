from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm,CustomUserChangeForm


# Create your views here.

# 로그인
@api_view(['POST'])
def login(request):
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
        # 만약 인증된 사용자라면 로그인 진행(세션 데이터 생성)
        # auth_login(request, 인증된 유저 객체)
        # auth_login(request, form.get_user()) <- 아래와 같은 코드
        user = form.get_user()
        auth_login(request,user)
        return  Response({"message": "Login successful", "user": user.username}, status=status.HTTP_200_OK)

    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


# 로그아웃
@api_view(['POST'])
@login_required
def logout(request):
    auth_logout(request)
    return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


# 회원가입
@api_view(['POST'])
def signup(request):
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        auth_login(request, user)
        return Response({"message": "Signup successful", "user": user.username}, status=status.HTTP_201_CREATED)
    return Response({"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)



#회원 탈퇴
@api_view(['DELETE'])
@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return Response({"message": "Account deleted"}, status=status.HTTP_200_OK)

#회원 정보 수정
@api_view(['PUT'])
@login_required
def update(request):
    form = CustomUserChangeForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        return Response({"message": "Account updated"}, status=status.HTTP_200_OK)
    return Response({"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)

# 비밀번호 수정
@api_view(['PUT'])
@login_required
def password_change(request):
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
        form.save()
        #비밀번호가 변경 됐다면 로그아웃(다시 로그인 페이지로 보내야함)
        auth_logout(request)
        return Response({"message": "Password changed, please log in again"}, status=status.HTTP_200_OK)
    return Response({"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)