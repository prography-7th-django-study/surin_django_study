from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'[{self.pk}]{self.name}'


class Brand(models.Model):
    name = models.CharField(max_length=50)
    categories = models.ManyToManyField(Category, related_name='brands')

    def __str__(self):
        return f'{self.name}'


class Size(models.Model):
    name = models.CharField(max_length=10)
    capacity = models.IntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}({self.brand})'


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    image = models.ImageField(upload_to='cafe/products/images')
    description = models.TextField()
    nutrition = models.JSONField(default=dict)
    hot_sizes = models.ManyToManyField(Size, blank=True, related_name='hot_sizes')
    ice_sizes = models.ManyToManyField(Size, blank=True, related_name='ice_sizes')
    is_limited = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    # 카테고리가 삭제된다고 모든 음료가 삭제되어야 할까?? 그럼 카테고리가 삭제되면 미분류로 되도록 설정하는 것으로 해야하나?
    # null을 허용하고 validation 처리를 하면 된다!! -> validation custom
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    # category - brand manytomany
    # category가 모델로 존재하지 않으면 존재하는 카테고리를 보고 싶을 때 모든 인스턴스에 접근해서 distinct를 해야하니까
    # 모델로서 존재하는 것이 낫다.
    total_score = models.FloatField(default=0, blank=True, editable=False)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='cafe/review/images', null=True, blank=True)


# 리뷰가 생성될 때마다 시그널을 받아 평점을 계산하는 함수 -> 나중에 리뷰가 엄청 많아질 경우에는 굉장히 오래 걸릴 코드이지만 현재는 괜찮음
@receiver(post_save, sender=Review)
def update_product_total_score(instance, **kwargs):
    product = instance.product
    product.total_score = product.reviews.all().aggregate(Avg('score')).get("score__avg")
    product.save()
