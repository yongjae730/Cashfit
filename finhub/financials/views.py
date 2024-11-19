from re import A
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from financials.models import FinancialComment,FinancialOptions,FinancialProducts,FinancialProductLike
from .serializers import FinancialProductsSerializer, FinancialOptionsSerializer, FinancialCommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from finhub import settings
import requests

# Create your views here.

User = get_user_model()

api_key = settings.API_KEY
# 정기 예금 API
DEPOSIT_BASE_URL = f"http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"
SAVING_BASE_URL = f"http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
# print(api_key)
# requests 모듈을 활용하여 정기 예금 상품 목록 데이터를
# 가져와 정기 예금 상품 목록과 옵션 목록을 DB에 저장
# 정기 예금정보'만'저장하는 상태
@api_view(['GET'])
def save_financial_products(request):
    DEPOSIT_URL = DEPOSIT_BASE_URL
    params = {
        'auth':api_key,
        'topFinGrpNo':'020000',
        'pageNo':1
    }
    
    deposit_response = requests.get(DEPOSIT_URL,params=params).json()
    SAVING_URL = SAVING_BASE_URL
    params = {
        'auth':api_key,
        'topFinGrpNo':'020000',
        'pageNo':1
    }
    
    saving_response = requests.get(SAVING_URL,params=params).json()
    # print(response)
    # 정기 예금 받아오기 
    for deposit_product_li in deposit_response.get('result').get('baseList'):
        fin_prdt_cd = deposit_product_li.get('fin_prdt_cd')
        fin_co_no = deposit_product_li.get('fin_co_no')
        kor_co_nm = deposit_product_li.get('kor_co_nm')
        fin_prdt_nm = deposit_product_li.get('fin_prdt_nm')
        etc_note = deposit_product_li.get('etc_note')
        join_deny = deposit_product_li.get('join_deny')
        join_member = deposit_product_li.get('join_member')
        join_way = deposit_product_li.get('join_way')
        spcl_cnd = deposit_product_li.get('spcl_cnd')


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

        deposit_save_product_data = {
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
        serializer = FinancialProductsSerializer(data=deposit_save_product_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for deposit_option_li in deposit_response.get('result').get('optionList'):

        fin_prdt_cd = deposit_option_li.get('fin_prdt_cd')
        intr_rate_type_nm = deposit_option_li.get('intr_rate_type_nm')
        intr_rate = deposit_option_li.get('intr_rate')
        intr_rate2 = deposit_option_li.get('intr_rate2')
        save_trm = deposit_option_li.get('save_trm')

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
    ## 적금 받아오기 
    for saving_product_li in saving_response.get('result').get('baseList'):
        fin_prdt_cd = saving_product_li.get('fin_prdt_cd')
        fin_co_no = saving_product_li.get('fin_co_no')
        kor_co_nm = saving_product_li.get('kor_co_nm')
        fin_prdt_nm = saving_product_li.get('fin_prdt_nm')
        etc_note = saving_product_li.get('etc_note')
        join_deny = saving_product_li.get('join_deny')
        join_member = saving_product_li.get('join_member')
        join_way = saving_product_li.get('join_way')
        spcl_cnd = saving_product_li.get('spcl_cnd')
        product_type = 1


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
            'spcl_cnd':spcl_cnd,
            "product_type" : product_type,
        }
        serializer = FinancialProductsSerializer(data=save_product_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for saving_option_li in saving_response.get('result').get('optionList'):

        fin_prdt_cd = saving_option_li.get('fin_prdt_cd')
        intr_rate_type_nm = saving_option_li.get('intr_rate_type_nm')
        intr_rate = saving_option_li.get('intr_rate')
        intr_rate2 = saving_option_li.get('intr_rate2')
        save_trm = saving_option_li.get('save_trm')

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
def deposit_top_rate(request):
    save_terms = [1,3,6,12,24,36]
    if request.method == "GET":
        deposit_highest_value_products = []
        for term in save_terms:
            options= FinancialOptions.objects.order_by('-intr_rate2').filter(save_trm = term)

            highest_option = None
            for option in options:
                if option.product.product_type == 0:
                    highest_option = option
                    break
            if highest_option:
                product = highest_option.product
                deposit_highest_value_products.append({
                "term": term,
                "product": FinancialProductsSerializer(product).data,
                "option": FinancialOptionsSerializer(highest_option).data,
            })

        return Response(deposit_highest_value_products, status=200)
    

@api_view(['GET'])
def saving_top_rate(request):
    save_terms = [1,3,6,12,24,36]
    if request.method == "GET":
        saving_highest_value_products = []
        for term in save_terms:
            options= FinancialOptions.objects.order_by('-intr_rate2').filter(save_trm = term)
            highest_option = None
            for option in options:
                if option.product.product_type == 1:
                    highest_option = option
                    break
            if highest_option:
                product = highest_option.product
                saving_highest_value_products.append({
                "term": term,
                "product": FinancialProductsSerializer(product).data,
                "option": FinancialOptionsSerializer(highest_option).data,
            })

        return Response(saving_highest_value_products, status=200)
    
    return Response({"error": "No options found"}, status=404)


### 상품에 대한 댓글 조회
@api_view(["GET"])
@permission_classes([AllowAny])
def financial_comment(request,fin_product_pk):
    product = get_object_or_404(FinancialProducts,pk=fin_product_pk)
    if request.method == "GET":
        #삭제되지 않은 댓글만 반환하려면 is_deleted=False 옵션
        comments = FinancialComment.objects.filter(financial_products=product)
        serializer = FinancialCommentSerializer(comments, many=True)
        return Response(serializer.data)
    
### 상품에 대한 댓글 생성
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def financial_comment_create(request,fin_product_pk):
    product = get_object_or_404(FinancialProducts,pk=fin_product_pk)
    if request.method == "POST":
        serializer = FinancialCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(users=request.user, financial_products=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        
# 댓글 수정 및 삭제
@api_view(["PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def update_delete_comment(request, comment_id):
    comment = get_object_or_404(FinancialComment, pk=comment_id, users=request.user)

    # 댓글 수정 로직
    if request.method == "PUT":
        serializer = FinancialCommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    # 댓글 삭제 로직
    elif request.method == "DELETE":
        comment.is_deleted = True
        comment.save()
        return Response({"message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

# 환율 정보 불러오기
def exchange_rate(request):
    BASE_URL = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
    API =settings.EXCHANGE_API_KEY
    params = {
        "authkey": API,
        "data": "AP01"
    }

    exchange_response = requests.get(BASE_URL,params=params).json()

    return JsonResponse({'exchange_rate':exchange_response}, status=200)

# 좋아요 기능
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def financial_product_like(request, product_id):
    product = get_object_or_404(FinancialProducts, id=product_id)
    user = request.user

    if request.method == 'POST':
        # 좋아요 추가
        like, created = FinancialProductLike.objects.get_or_create(user=user, product=product)
        if created:
            return Response({"message": "Liked successfully."}, status=status.HTTP_201_CREATED)
        return Response({"message": "Already liked."}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        # 좋아요 삭제
        like = get_object_or_404(FinancialProductLike, user=user, product=product)
        like.delete()
        return Response({"message": "Unliked successfully."}, status=status.HTTP_204_NO_CONTENT)

# 유저 프로필 페이지에서 좋아요 한 상품 목록 출력
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_liked_products(request):
    user = request.user
    likes = FinancialProductLike.objects.filter(user=user)
    serializer = FinancialProductsSerializer([like.product for like in likes], many=True)
    return Response(serializer.data)