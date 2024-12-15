from django.urls import path
from .views import ProductListView

urlpatterns = [
    # 상품 리스트 API
    path('', ProductListView.as_view(), name='product-list'),
]
