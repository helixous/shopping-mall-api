from typing import Optional

from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Coupon
from .serializers import ProductItemSerializer

# 상품 리스트 뷰 (CBV)
class ProductListView(generics.ListAPIView):
    serializer_class = ProductItemSerializer

    def get_queryset(self):
        """
        상품 쿼리셋 반환 메서드 (카테고리 필터링 가능)
        :return: 상품 QuerySet
        """
        self.request: Request
        category_id: Optional[str] = self.request.query_params.get('category')
        queryset = Product.objects.all().select_related('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset
