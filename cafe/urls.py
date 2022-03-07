from django.urls import path
from cafe import views
urlpatterns = [
    path('', views.brand_list),
    path('<int:pk>', views.brand_detail),
    path('<int:pk>/products', views.product_list),
    #path('<int:pk>/products/<int:pk>', views.product_detail),
]