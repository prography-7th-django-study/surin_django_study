
from cafe.models import Brand, Product
from cafe.serializer import *
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from cafe.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
# Create your views here.


# 브랜드 뷰
class BrandViewSet(ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


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
        category = self.get_object().categories.get(pk=pk)
        products = Product.objects.filter(brand=self.get_object(), category=category).all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


# 상품 뷰
class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [
        IsAdminUser,
    ]

    def get_queryset(self):
        return Product.objects.filter(brand=Brand.objects.get(pk=self.kwargs.get("brand_pk"))).all()


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
        obj = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        if obj:
            return Review.objects.filter(product=obj).all()
        return obj


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
