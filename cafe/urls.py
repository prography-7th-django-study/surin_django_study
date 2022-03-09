from django.urls import path
from cafe import views
urlpatterns = [
    path('brands', views.brand_list),
    path('brands/<int:pk>', views.brand_detail),
    path('brands/<int:brand_pk>/categories', views.category_list),
    path('brands/<int:brand_pk>/categories/<int:pk>', views.CategoryDetailAPIView.as_view()),
    path('brands/<int:brand_pk>/products', views.product_list),
    path('brands/<int:brand_pk>/products/<int:pk>', views.product_detail),
    path('brands/<int:pk>/products/limit', views.ProductLimitedListView.as_view()),
    path('brands/<int:brand_pk>/products/<int:product_pk>/reviews', views.review_list),
    path('brands/<int:brand_pk>/products/<int:product_pk>/reviews/<int:pk>', views.review_detail),
    path('me/reviews', views.user_review_list),
    path('me/reviews/<int:pk>', views.user_review_detail),
]
