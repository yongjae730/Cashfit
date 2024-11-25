from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # 닉네임
    nickname = models.CharField(max_length=50, blank=True, default="")  # 올바르게 설정
    # 나이
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name="나이")
    # 자본금 (만원 단위)
    capital = models.PositiveIntegerField(null=True, blank=True, verbose_name="자본금")
    # 지역
    sido = models.CharField(max_length=10)
    sigungus = models.CharField(max_length=10)

    
    # user 출력 시 닉네임으로 나오게
    def __str__(self):
        return self.nickname