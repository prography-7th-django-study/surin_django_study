from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from cafe.models import Brand, Category, Product, Review, Size

# to_representation 사용하는 것은 비추천
# serializer method field
# related field


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            return None
        return user


class UserSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    hot_sizes = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    ice_sizes = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    category = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    total_score = serializers.DecimalField(decimal_places=2, max_digits=5)

    class Meta:
        model = Product
        fields = [
            'name',
            'price',
            'image',
            'description',
            'nutrition',
            'hot_sizes',
            'ice_sizes',
            'is_limited',
            'category',
            'brand',
            'total_score',
        ]

    def get_category(self, obj):
        return obj.category.name

    def get_brand(self, obj):
        return obj.brand.name


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Category
        fields = [
            'name',
        ]


class BrandSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    score = serializers.DecimalField(decimal_places=2, max_digits=5)

    class Meta:
        model = Brand
        fields = [
            'name',
            'categories',
            'score'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y년 %m월 %d일")

    class Meta:
        model = Review
        fields = [
            'product',
            'content',
            'score',
            'author',
            'created_at',
            'image',
        ]

    def get_product(self, obj):
        return obj.product.name

    def get_author(self, obj):
        return obj.author.username


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = [
            'name',
        ]

