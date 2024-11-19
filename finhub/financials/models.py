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


class ExchangeRate(models.Model):
    # 통화 코드
    cur_unit = models.TextField()
    # 국가/통화명
    cur_nm = models.TextField()
    # 전신환(송금) 받으실 때 (고객의 입장에서 외환을 받을 때)
    ttb = models.FloatField()
    # 전신환(송금) 보내실 때 (고객의 입장에서 외환을 보낼 때)
    tts = models.FloatField()
    # 매매 기준율 (최근 거래일에 외국환중개회사를 통하여 거래가 이루어진 
    # 미달러화의 현물환율을 거래량으로 가중 평균하여 산출되는 시장평균환율)
    deal_bas_r = models.FloatField()
    # 장부 가격 (외국환은행이 대고객 외국환거래에 따르
    # 는 수수료를 원화로 징수할 때 적용하는 환율)
    bkpr = models.FloatField()
    # 년 환가료율 (외국환을 사고 팔때 외국환은행이 자금부담에 따른 이자 성격으로 고객에게 징수하는 일종의 수수료)
    yy_efee_r = models.FloatField()
    # 10일환가료율
    ten_dd_efee_r = models.FloatField()
    # 서울외국환중개 장부 가격
    # 기업이 보유한 외화 자산이나 부채를 회계 장부에 기록할 때 적용하는 환율
    kftc_bkpr = models.FloatField()
    # 서울외국환중개 매매 기준율
    # (외국환중개 회사를 통해 거래된 미 달러화와 위환화 각각 현물환 거래량을
    # 가중평균하여 산출되는 시장평균환율)
    kftc_deal_bas_r = models.FloatField()