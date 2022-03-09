
from cafe.models import Brand, Product
from cafe.serializer import *
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.http import Http404
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Avg
# Create your views here.


# 브랜드 뷰
class BrandViewSet(ReadOnlyModelViewSet):
    #queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get_queryset(self):
        brands = Brand.objects.annotate(score=Avg('products__total_score'))
        return brands.order_by('-score')


brand_list = BrandViewSet.as_view({
    'get': 'list',
})
brand_detail = BrandViewSet.as_view({
    'get': 'retrieve',
})


# 카테고리 뷰
class CategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        query = Brand.objects.get(pk=self.kwargs.get('brand_pk'))
        return query.categories.all()


category_list = CategoryViewSet.as_view({
    'get': 'list',
})


class CategoryDetailAPIView(APIView):

    def get_object(self):
        return Brand.objects.get(pk=self.kwargs.get('brand_pk'))

    def get(self, request, pk, **kwargs):
        try:
            category = self.get_object().categories.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404("Not Found")
        products = Product.objects.filter(brand=self.get_object(), category=category).all().order_by('-total_score')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


# 상품 뷰
class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [
        IsAdminUser,
    ]

    def get_queryset(self):
        return Product.objects.filter(brand=Brand.objects.get(pk=self.kwargs.get("brand_pk"))).all().order_by('-total_score')


product_list = ProductViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
product_detail = ProductViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})


class ProductLimitedListView(generics.ListAPIView, GenericAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        obj = Brand.objects.get(pk=self.kwargs.get('pk'))
        return Product.objects.filter(brand=obj, is_limited=True)


# 리뷰 뷰
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        brand_pk = self.kwargs['brand_pk']
        product_pk = self.kwargs['product_pk']
        return Review.objects.filter(product_id=product_pk, product__brand_id=brand_pk).order_by('-score')


review_list = ReviewViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

review_detail = ReviewViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})


class UserReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]

    def get_queryset(self):
        return Review.objects.filter(author=self.request.user).order_by('-score')


user_review_list = UserReviewViewSet.as_view({
    'get': 'list',
})

user_review_detail = UserReviewViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
