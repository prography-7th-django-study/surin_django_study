from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class Brand(models.Model):
    name = models.CharField(max_length=50)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    image = models.ImageField(upload_to='cafe/products/images')
    description = models.TextField()
    nutrition = models.JSONField(default=dict)
    hot_size = models.TextField(help_text='쉼표(,)를 구분자로 작성해주세요.', blank=True, default="")
    ice_size = models.TextField(help_text='쉼표(,)를 구분자로 작성해주세요.', blank=True, default="")
    is_limited = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    # 카테고리가 삭제된다고 모든 음료가 삭제되어야 할까?? 그럼 카테고리가 삭제되면 미분류로 되도록 설정하는 것은 현명할까..?
    # null을 허용하고 validation 처리를 하면 된다!! -> validation customize
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    # category - brand manytomany
    # category가 모델로 존재하지 않으면 존재하는 카테고리를 보고 싶을 때 모든 인스턴스에 접근해서 distinct를 해야하니까
    # 모델로서 존재하는 것이 더 좋겠지??

    def __str__(self):
        return f'{self.name}'


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField()
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='cafe/review/images', null=True)
