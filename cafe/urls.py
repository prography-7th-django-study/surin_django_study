from django.urls import path
from cafe import views
urlpatterns = [
    path('', views.brand_list),
    path('<int:pk>', views.brand_detail),
    path('<int:pk>/categories', views.category_list),
    #path('<int:brand_pk>/categories/<int:pk>/products', views.category_detail),
    path('<int:brand_pk>/products', views.product_list),
    path('<int:brand_pk>/products/<int:pk>', views.product_detail),
]
