from django.urls import path
from .views import ProductListView, get_product_detail, CategoryListView, CouponListView

urlpatterns = [
    # 상품 리스트 API (CBV)
    path('', ProductListView.as_view(), name='product-list'),
    # 상품 상세 페이지 API (FBV)
    path('<int:pk>/', get_product_detail, name='product-detail'),
    # 카테고리 리스트 API (CBV)
    path('categories/', CategoryListView.as_view(), name='category-list'),
    # 쿠폰 리스트 API (CBV)
    path('coupons/', CouponListView.as_view(), name='coupon-list'),
]
