from decimal import Decimal

from django.db import models


class Category(models.Model):
    name = models.CharField(
        verbose_name='카테고리 이름',
        max_length=100,
    )

    def __str__(self):
        return self.name


class Coupon(models.Model):
    code = models.CharField(
        verbose_name='쿠폰 코드',
        max_length=50,
        unique=True,
    )

    # 최대 100.00% 을 표현할 수 있는
    # Decimal 필드로 선언
    discount_rate = models.DecimalField(
        verbose_name='쿠폰 할인율',
        max_digits=5,
        decimal_places=2,
    )

    def __str__(self):
        return self.code


class Product(models.Model):
    name = models.CharField(
        verbose_name='상품 이름',
        max_length=255,
    )

    description = models.TextField(
        verbose_name='상품 설명'
    )

    price = models.PositiveIntegerField(
        verbose_name='상품 가격(원)'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='상품 카테고리'
    )

    discount_rate = models.DecimalField(
        verbose_name='할인율',
        max_digits=5,
        decimal_places=2,
        default=0.00
    )

    coupon_applicable = models.BooleanField(
        verbose_name='쿠폰 적용 가능 여부',
        default=False
    )

    def calc_discounted_price(self) -> int:
        """
        할인율이 적용된 상품가격 반환기
        :return:
        """
        result: Decimal = self.price * Decimal(1 - self.discount_rate)
        return int(result)

    def calc_coupon_applied_price(self, coupon: 'Coupon') -> int:
        """
        쿠폰 할인율이 적용된 최종 가격 반환
        :param coupon: 적용할 쿠폰 객체
        :return: 쿠폰 할인율이 적용된 가격 (int)
        """
        discounted_price: int = self.calc_discounted_price()
        # 상품에 쿠폰이 적용 가능할 경우에 쿠폰 할인율을 적용한다.
        if self.coupon_applicable:
            result: Decimal = discounted_price * Decimal(1 - coupon.discount_rate)
            return int(result)
        # 쿠폰 적용 불가능할 경우 상품 자체 할인율만 적용된 금액 리턴
        return discounted_price

    def __str__(self):
        return self.name
