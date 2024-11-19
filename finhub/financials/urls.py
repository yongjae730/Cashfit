from django.urls import path
from . import views


app_name = 'financials'
urlpatterns = [
    # 정기 예금 상품 목록 DB에 저장
    path('save-financial-products/', views.save_financial_products),
    # 전체 정기 예금 상품 목록 출력 & 데이터 삽입
    path('financial-products/', views.financial_products),
    # 특정 상품의 옵션 리스트 출력
    path('financial-product-options/<str:fin_product_cd>/', views.financial_product_options),
    # 가입 기간에 상관 없이 최고 금리가 가장 높은 금융상품과
    # 해당 상품의 옵션 리스트 출력
    path('financial-products/deposit_top_rate/', views.deposit_top_rate),
    path('financial-products/saving_top_rate/', views.saving_top_rate),
    # 댓글 조회 url
    path('financial-comment/<int:fin_product_pk>/', views.financial_comment),
    path('financial_comment_create/<int:fin_product_pk>/', views.financial_comment_create),
    # 댓글 수정 및 삭제 url
    path('financial-comment/update-delete/<int:comment_id>/', views.update_delete_comment),    
    # 좋아요 기능
    path('products/<int:product_id>/like/', views.financial_product_like),
    # 좋아요를 누른 상품 목록
    path('profile/liked-products/', views.user_liked_products),

    # 환율 정보 DB에 저장
    path('exchange-rate/', views.exchange_rate),
]
