from rest_framework import serializers
from .models import Product, Category


class ProductItemSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'discounted_price',
            'category',
            'coupon_applicable'
        )

    def get_discounted_price(self, instance: Product) -> int:
        """
        할인된 가격 반환 메서드
        Product 모델의 할인된 가격 반환 메서드를 호출
        :param instance: Product 객체
        :return: 할인된 가격 (int)
        """
        result = instance.calc_discounted_price()
        return result


class CategoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name'
        )
