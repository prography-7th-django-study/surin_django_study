from django.urls import path, include
from rest_framework.routers import SimpleRouter
from cafe.views import *

# ViewSet은 여러가지 요청을 담고 있는 확장형이기 때문에 router를 사용하는 것
# 라우터가 경로별로 뿌려주는 역할을 하기 때문에 사용한다.
# 관계가 깊은 url을 라우터로 연결할 때에도 경로를 지정하여 라우터를 만들어줘야 한다.
# 그래도 라우터를 사용하는 것이 덜 복잡하고, 자동화가 되니까!
# 그리고 확장성도 더욱 크기 때문이다.
brand_router = SimpleRouter(trailing_slash=False)
brand_router.register('brands', BrandViewSet, basename='Brand')

user_router = SimpleRouter(trailing_slash=False)
user_router.register('me/reviews', UserReviewViewSet, basename='User-Reviews')

brand_category_router = SimpleRouter(trailing_slash=False)
brand_category_router.register('/categories', BrandCategoryViewSet, basename='Brand-Categories')

brand_category_products_router = SimpleRouter(trailing_slash=False)
brand_category_products_router.register('/products', BrandCategoryProductViewSet, basename='Brand-Category-Products')

brand_products_router = SimpleRouter(trailing_slash=False)
brand_products_router.register('/products', BrandProductViewSet, basename='Brand-Product')

brand_product_reviews_router = SimpleRouter(trailing_slash=False)
brand_product_reviews_router.register('/reviews', BrandProductReviewViewSet, basename='Brand-Product-Reviews')


urlpatterns = [
    path('', include(brand_router.urls)),
    path('brands/<int:brand_pk>', include(brand_category_router.urls)),
    path('brands/<int:brand_pk>/categories/<int:category_pk>', include(brand_category_products_router.urls)),
    path('brands/<int:brand_pk>', include(brand_products_router.urls)),
    path('brands/<int:brand_pk>/products/<int:product_pk>', include(brand_product_reviews_router.urls)),
    path('', include(user_router.urls)),
]
