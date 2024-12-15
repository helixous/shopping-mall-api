from typing import Optional, Union, Any, Dict

from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Product, Coupon, Category
from .serializers import ProductListSerializer, ProductDetailSerializer, CategoryItemSerializer, CouponItemSerializer
from .utils import api_response


# 상품 리스트 뷰 (CBV)
class ProductListView(generics.ListAPIView):
    """
    상품 리스트 조회 API
    """
    serializer_class = ProductListSerializer

    def get_queryset(self):
        """
        상품 쿼리셋 반환 메서드 (카테고리 필터링 가능)
        :return: 상품 QuerySet
        """
        self.request: Request
        category_id: Optional[str] = self.request.query_params.get('category_id')
        queryset = Product.objects.all().select_related('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        상품 리스트 API 응답 형식 통일
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return api_response(
            status_code=status.HTTP_200_OK,
            message="Success",
            data=serializer.data
        )


# 상품 상세 뷰 (FBV)
@api_view(["GET"])
def get_product_detail(request, pk: int) -> Response:
    """
    상품 상세 조회 API
    - 쿠폰 코드 적용 가능
    """
    try:
        product = Product.objects.select_related("category").get(pk=pk)
    except Product.DoesNotExist:
        return api_response(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Product not found",
            data=None
        )

    # 쿠폰 처리
    coupon_code: Optional[str] = request.query_params.get("coupon_code")
    coupon_instance = None
    if coupon_code:
        try:
            coupon_instance = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            return api_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Invalid coupon code",
                data=None
            )

    # 직렬화 및 응답
    context = {
        "coupon_instance": coupon_instance
    }

    serializer = ProductDetailSerializer(
        instance=product,
        context=context
    )

    return api_response(
        status_code=status.HTTP_200_OK,
        message="Success",
        data=serializer.data
    )


# 카테고리 리스트 뷰 (CBV)
class CategoryListView(APIView):
    """
    카테고리 리스트 API
    """

    def get(self, request: Request) -> Response:
        """
        모든 카테고리 리스트 반환
        """
        queryset = Category.objects.all()

        serializer = CategoryItemSerializer(
            instance=queryset,
            many=True
        )

        return api_response(
            status_code=status.HTTP_200_OK,
            message="Success",
            data=serializer.data
        )


# 쿠폰 리스트 뷰 (CBV)
class CouponListView(APIView):
    """
    쿠폰 리스트 API
    """

    def get(self, request: Request) -> Response:
        """
        모든 쿠폰 리스트 반환
        """
        queryset = Coupon.objects.all()

        serializer = CouponItemSerializer(
            instance=queryset,
            many=True
        )

        return api_response(
            status_code=status.HTTP_200_OK,
            message="Success",
            data=serializer.data
        )
