from django.urls import path
from cafe import views
urlpatterns = [
    path('', views.brand_list),
    path('<int:pk>', views.brand_detail),
    path('<int:brand_pk>/categories', views.category_list),
    path('<int:brand_pk>/categories/<int:pk>', views.CategoryDetailAPIView.as_view()),
    path('<int:brand_pk>/products', views.product_list),
    path('<int:brand_pk>/products/<int:pk>', views.product_detail),
    path('<int:pk>/products/limit', views.ProductLimitedListView.as_view()),
    path('<int:brand_pk>/products/<int:pk>/reviews', views.review_list),
]
