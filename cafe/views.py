from rest_framework.decorators import action
from rest_framework.response import Response
from cafe.authentications import get_token
from cafe.filters import LimitedProductFilter
from cafe.serializer import *
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Avg
from rest_framework import filters
from rest_framework.generics import GenericAPIView
# Create your views here.


class BrandViewSet(ReadOnlyModelViewSet):
    serializer_class = BrandSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'score']

    def get_queryset(self):
        # serializer에 score 필드가 선언되어 있어야 annotate로 받은 값이 들어가서 활용이 가능해진다 ?!
        query = Brand.objects.annotate(score=Avg('products__total_score'))
        return query


class BrandCategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        query = Brand.objects.get(pk=self.kwargs.get('brand_pk'))
        return query.categories.all()


class BrandCategoryProductViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['total_score', 'name']

    def get_queryset(self):
        return Product.objects.filter(brand=self.kwargs['brand_pk'], category=self.kwargs['category_pk'])


# 상품 뷰
class BrandProductViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    # 어차피 상품 등록, 수정 및 삭제는 어드민 사이트에서 할 것이기 때문에 굳이 put, post 메소드를 사용할 필요가 없다.
    filter_backends = [filters.OrderingFilter, LimitedProductFilter]
    ordering_fields = ['total_score', 'name']
    # filters.py -> Ordering Filter custom -> limit=True parameter 사용하는 것도 방법

    def get_queryset(self):
        return Product.objects.filter(brand=Brand.objects.get(pk=self.kwargs.get("brand_pk"))).all()

    # 데코레이터 사용 vs parameter 사용
    # @action(detail=False, url_path='limited')
    # def get_limitation(self, request, **kwargs):
    #     limited_products = Product.objects.filter(brand=Brand.objects.get(pk=kwargs.get("brand_pk")), is_limited=True).all()
    #     serializer = self.get_serializer(limited_products, many=True)
    #     return Response(serializer.data, status=200)


# 리뷰 뷰
class BrandProductReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['score']

    def get_queryset(self):
        brand_pk = self.kwargs['brand_pk']
        product_pk = self.kwargs['product_pk']
        return Review.objects.filter(product_id=product_pk, product__brand_id=brand_pk)


class UserReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticated
    ]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['score']

    def get_queryset(self):
        return Review.objects.filter(author=self.request.user)


class LoginView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        user = self.get_serializer().validate(request.data)
        if user is None:
            return Response(status=400)
        token = get_token(user)
        return Response(token, status=200)


class SignUpView(GenericAPIView):
    serializer_class = UserSignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        serializer.create(serializer.data)
        return Response('SignUp Succeed!', status=200)
