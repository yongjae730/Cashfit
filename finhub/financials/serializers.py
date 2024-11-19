from rest_framework import serializers
from .models import FinancialProducts,FinancialOptions,FinancialComment,FinancialProductLike



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
    class FinancialCommentProductInfo(serializers.ModelSerializer):
        class Meta:
            model = FinancialProducts
            fields = "__all__"

    financial_products = FinancialCommentProductInfo(read_only=True)

    class Meta:
        model = FinancialComment
        fields = "__all__"
        read_only_fields = ('users',)
        # read_only_fields = ('users', 'financial_products')

class FinancialProductLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialProductLike
        fields = ('user', 'product', 'created_at',)
        read_only_fields = ('user', 'created_at',)