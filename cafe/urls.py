from django.urls import path
from cafe import views
urlpatterns = [
    path('', views.BrandListMixins.as_view()),
    path('<int:pk>', views.BrandDetailMixins.as_view()),
    path('<int:pk>/products', views.ProductListAPI.as_view()),
]