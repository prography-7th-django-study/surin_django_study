
from cafe.models import Brand, Product
from cafe.serializer import BrandSerializer, ProductSerializer, CategorySerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.contrib.auth.models import User
from cafe.permissions import IsAdminUser
# Create your views here.
"""@csrf_exempt
@api_view(['GET', 'POST'])
def brand_list(request):
    if request.method == 'GET':
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)"""

"""class BrandListAPIView(APIView):
    def get(self, request):
        serializer = BrandSerializer(Brand.objects.all(), many=True) # 여러개 가져오므로
        return Response(serializer.data)"""


"""class BrandListMixins(ListModelMixin, GenericAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request)"""

"""class BrandDetailAPI(APIView):
    def get_object(self, pk):
        return get_object_or_404(Brand, pk=pk)

    def get(self, request, pk):
        serializer = BrandSerializer(self.get_object(pk=pk))
        return Response(serializer.data)
        
    class BrandDetailMixins(RetrieveModelMixin, GenericAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request)
"""


"""class ProductListAPI(APIView):
    def get_brand_object(self, pk):
        return get_object_or_404(Brand, pk=pk)

    def get(self, request, pk):
        serializer = ProductSerializer(Product.objects.filter(brand=self.get_brand_object(pk=pk)), many=True)
        return Response(serializer.data)"""


"""class ProductListMixins(ListModelMixin, GenericAPIView, RetrieveModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request)"""


class BrandViewSet(ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


brand_list = BrandViewSet.as_view({
    'get':'list',
})
brand_detail = BrandViewSet.as_view({
    'get':'retrieve',
})


class CategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        query = Brand.objects.get(pk=self.kwargs.get('brand_pk'))
        return query.category.all()


category_list = CategoryViewSet.as_view({
    'get':'list',
})


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [
        IsAdminUser,
    ]

    def get_queryset(self):
        return Product.objects.filter(brand=Brand.objects.get(pk=self.kwargs.get("brand_pk"))).all()


product_list = ProductViewSet.as_view({
    'get':'list',
    'post':'create',
})
product_detail = ProductViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'patch':'partial_update',
    'delete':'destroy',
})
