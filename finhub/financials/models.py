from django.db import models
from django.contrib.auth import get_user_model

import financials
User = get_user_model()


# Create your models here.
class FinancialProducts(models.Model):
    # 금융 회사 코드 (7차에 없던 것 추가 한거라 작동 제대로 되는지 확인해야함)
    fin_co_no = models.TextField()
    # 금융 상품 코드
    fin_prdt_cd = models.TextField()
    # 금융 회사 명
    kor_co_nm = models.TextField()
    # 금융 상품 명
    fin_prdt_nm = models.TextField()
    # 금융 상품 설명
    etc_note = models.TextField()
    # 가입제한(1:제한없음,2:서민전용,3:일부제한)
    join_deny = models.IntegerField()
    # 가입대상
    join_member = models.TextField()
    # 가입 방법
    join_way = models.TextField()
    # 우대 조건
    spcl_cnd = models.TextField()
    # 예금 적금 판단할 수 있는 변수 ex. 예금은 0 적금은 1
    product_type = models.IntegerField(default=0)

class FinancialOptions(models.Model):
    # 외래 키(FinancialProducts 클래스 참조)
    product = models.ForeignKey(FinancialProducts, on_delete=models.CASCADE, related_name="option")
    # 금융 상품 코드
    fin_prdt_cd = models.TextField()
    # 적립 유형 명 (적금에만 존재)
    rsrv_type_nm = models.TextField(null=True,blank=True)
    # 저축 금리 유형명
    intr_rate_type_nm = models.CharField(max_length=100)
    # 저축 금리
    intr_rate = models.FloatField(null=True)
    # 최고 우대 금리
    intr_rate2 = models.FloatField()
    # 저축 기간(단위:개월)
    save_trm = models.IntegerField()


class FinancialComment(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name='financial_comments')
    financial_products = models.ForeignKey(FinancialProducts, on_delete=models.CASCADE, related_name='financial_product_comments')
    content = models.CharField(max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
