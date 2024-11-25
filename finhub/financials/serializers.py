from rest_framework import serializers
from .models import FinancialProducts,FinancialOptions,FinancialComment,FinancialProductLike,ExchangeRate



class FinancialProductsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FinancialProducts
        fields = "__all__"

class FinancialOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialOptions
        fields = "__all__"
        read_only_fields = ('product',)

class FinancialCommentSerializer(serializers.ModelSerializer):

    nickname = serializers.CharField(source='users.nickname', read_only=True)

    class Meta:
        model = FinancialComment
        fields = ('id', 'content', 'users', 'nickname', 'financial_products', 'create_at', 'is_deleted')
        read_only_fields = ('users', 'financial_products')

class FinancialProductLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialProductLike
        fields = ('user', 'product', 'created_at',)
        read_only_fields = ('user', 'created_at',)


### 전체 상품과 옵션을 추가하는 시리얼라이저들

class FinancialOptionsSimpleSerializer(serializers.ModelSerializer): # 옵션데이터를 간단히 직렬화하는 시리얼라이저
    class Meta:
        model = FinancialOptions
        fields = ("intr_rate_type_nm", "intr_rate", "intr_rate2", "save_trm","rsrv_type_nm")

class FinancialProductWithOptionsSerializer(serializers.ModelSerializer): #기본 상품 필드 외에 옵션 데이터를 포함하는 시리얼라이저
    options = serializers.SerializerMethodField()  # 옵션 데이터를 추가하는 필드

    class Meta:
        model = FinancialProducts
        fields = "__all__"

    def get_options(self, obj):
        options = FinancialOptions.objects.filter(product=obj)  # 해당 상품의 옵션 가져오기
        return FinancialOptionsSimpleSerializer(options, many=True).data


class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = "__all__"