from typing import Union

from rest_framework import serializers
from .models import Product, Category, Coupon


class ProductListSerializer(serializers.ModelSerializer):
    """
    상품 리스트 조회 API 응답 시리얼라이저
    """
    category = serializers.StringRelatedField()  # 카테고리 이름만 반환

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "category",
            "discount_rate",
            "coupon_applicable",
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    상품 상세정보 조회 API 응답 시리얼라이저
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            # 쿠폰 객체관련 반복연산 방지를 위해 __init__ 에서 한번에 연산
            self.coupon_instance: Union[Coupon, None] = self.context.get('coupon_instance')
            self.is_coupon_applied_val = False
            if self.coupon_instance:
                self.is_coupon_applied_val = True

    def get_original_price(self, instance: Product) -> int:
        """
        원래 가격 반환기
        """
        return instance.price

    def get_discounted_price(self, instance: Product) -> int:
        """
        상품 자체 할인율 적용 가격 반환기
        """
        return instance.calc_discounted_price()

    def get_final_price(self, instance: Product) -> int:
        """
        최종 가격 반환기 (자체할인율, 쿠폰할인율)
        """
        if self.coupon_instance:
            return instance.calc_coupon_applied_price(self.coupon_instance)
        return instance.calc_discounted_price()

    def get_is_coupon_applied(self, instance: Product) -> bool:
        """
        쿠폰이 실제로 적용되었는지 여부 판단(필요할 것 같아 추가하였습니다)
        """
        return self.is_coupon_applied_val

    original_price = serializers.SerializerMethodField()
    discounted_price = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    is_coupon_applied = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'discount_rate',
            'original_price',
            'discounted_price',
            'final_price',
            'is_coupon_applied',
            'category',
            'coupon_applicable',
        )


class CategoryItemSerializer(serializers.ModelSerializer):
    """
    카테고리 리스트 조회 API 응답 시리얼라이저
    """
    class Meta:
        model = Category
        fields = (
            'id',
            'name'
        )


class CouponItemSerializer(serializers.ModelSerializer):
    """
    쿠폰 리스트 조회 API 응답 시리얼라이저
    """
    class Meta:
        model = Coupon
        fields = (
            "id",
            "code",
            "discount_rate"
        )
