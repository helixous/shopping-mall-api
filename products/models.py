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

    def __str__(self):
        return self.name
