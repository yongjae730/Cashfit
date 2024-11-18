from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # 닉네임
    nickname = models.CharField(max_length=10)
    # 나이
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name="나이")
    # 자본금 (만원 단위)
    capital = models.PositiveIntegerField(null=True, blank=True, verbose_name="자본금")
    

    # user 출력 시 유저 이름으로 나오게
    def __str__(self):
        return self.username