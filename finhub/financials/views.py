# Create your views here.
# from bson import is_valid
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
import requests
from rest_framework.decorators import api_view
from financials.models import FinancialComment,FinancialOptions,FinancialProducts
from finhub import settings
from .serializers import FinancialProductsSerializer, FinancialOptionsSerializer, FinancialCommentSerializer
from rest_framework import status
from django.contrib.auth import get_user_model
# Create your views here.
from pprint import pprint

User = get_user_model()

api_key = settings.API_KEY
# 정기 예금 API
BASE_URL = f"http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"
# print(api_key)
# requests 모듈을 활용하여 정기 예금 상품 목록 데이터를
# 가져와 정기 예금 상품 목록과 옵션 목록을 DB에 저장
# 정기 예금정보'만'저장하는 상태
@api_view(['GET'])
def save_financial_products(request):
    URL = BASE_URL
    params = {
        'auth':api_key,
        'topFinGrpNo':'020000',
        'pageNo':1
    }
    
    response = requests.get(URL,params=params).json()
    # print(response)
    for product_li in response.get('result').get('baseList'):
        fin_prdt_cd = product_li.get('fin_prdt_cd')
        fin_co_no = product_li.get('fin_co_no')
        kor_co_nm = product_li.get('kor_co_nm')
        fin_prdt_nm = product_li.get('fin_prdt_nm')
        etc_note = product_li.get('etc_note')
        join_deny = product_li.get('join_deny')
        join_member = product_li.get('join_member')
        join_way = product_li.get('join_way')
        spcl_cnd = product_li.get('spcl_cnd')


        if FinancialProducts.objects.filter(
            fin_prdt_cd=fin_prdt_cd,
            kor_co_nm=kor_co_nm,
            fin_prdt_nm=fin_prdt_nm,
            etc_note=etc_note,
            fin_co_no=fin_co_no,
            join_deny=join_deny,
            join_member=join_member,
            join_way=join_way,
            spcl_cnd=spcl_cnd).exists():
            continue
        save_product_data = {
            'fin_prdt_cd':fin_prdt_cd,
            'kor_co_nm':kor_co_nm,
            'fin_prdt_nm':fin_prdt_nm,
            'fin_co_no':fin_co_no,
            'etc_note':etc_note,
            'join_deny':join_deny,
            'join_member':join_member,
            'join_way':join_way,
            'spcl_cnd':spcl_cnd
        }
        serializer = FinancialProductsSerializer(data=save_product_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for option_li in response.get('result').get('optionList'):

        fin_prdt_cd = option_li.get('fin_prdt_cd')
        intr_rate_type_nm = option_li.get('intr_rate_type_nm')
        intr_rate = option_li.get('intr_rate')
        intr_rate2 = option_li.get('intr_rate2')
        save_trm = option_li.get('save_trm')

        product = FinancialProducts.objects.get(fin_prdt_cd=fin_prdt_cd)

        if not intr_rate :
            intr_rate = -1

        if FinancialOptions.objects.filter(
            fin_prdt_cd=fin_prdt_cd,
            intr_rate_type_nm=intr_rate_type_nm,
            intr_rate=intr_rate,
            intr_rate2=intr_rate2,
            save_trm=save_trm).exists():
            continue

        save_option_data = {
            'fin_prdt_cd':fin_prdt_cd,
            'intr_rate_type_nm':intr_rate_type_nm,
            'intr_rate':intr_rate,
            'intr_rate2':intr_rate2,
            'save_trm':save_trm,
        }
        serializer = FinancialOptionsSerializer(data=save_option_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(product=product)

    return JsonResponse({'message':'저장완료'})

# GET : 전체 정기 예금 상품 목록 반환
# POST : 상품 데이터 저장
@api_view(['GET','POST'])
def financial_products(request):
    if request.method == 'GET':
        products = FinancialProducts.objects.all()
        serializer = FinancialProductsSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FinancialProductsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            Response(serializer.data, status=status.HTTP_201_CREATED)


# 특정 상품의 옵션 리스트 반환
@api_view(['GET'])
def financial_product_options(request,fin_product_cd):
    if request.method == 'GET':
        product = FinancialOptions.objects.filter(fin_prdt_cd=fin_product_cd)
        serializer = FinancialOptionsSerializer(product, many=True)
        return Response(serializer.data)

# 가입 기간에 상관 없이 금리가 가장 높은 상품과
# 해당 상품의 옵션 리스트 출력
@api_view(['GET'])
def top_rate(request):
    
    if request.method == "GET":
        highest_value_product_option = FinancialOptions.objects.order_by('-intr_rate2').first()
        highest_value_product = highest_value_product_option.product
        option_serializer = FinancialOptionsSerializer(highest_value_product_option)
        product_serializer = FinancialProductsSerializer(highest_value_product)

        return Response({
            "Financial_product": product_serializer.data,
            "option": option_serializer.data,
        })
    return Response({"error": "No options found"}, status=404)

### 상품에 대한 댓글 생성 및 조회
@api_view(["GET","POST"])
def financial_comment(request,fin_product_pk):
    product = get_object_or_404(FinancialProducts,pk=fin_product_pk)
    if request.method == "GET":
        #삭제되지 않은 댓글만 반환하려면 is_deleted=False 옵션
        comments = FinancialComment.objects.filter(financial_products=product)
        serializer = FinancialCommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = FinancialCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # 임시 유저 할당
            temp_user = User.objects.first()  # 첫 번째 유저를 임시로 할당
            serializer.save(users=temp_user, financial_products=product)
            # serializer.save(users=request.user, financial_product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)