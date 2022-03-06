from django.urls import path
from cafe import views
urlpatterns = [
    path('', views.BrandListAPIView.as_view()),
    path('<int:pk>', views.BrnadDetailAPI.as_view()),
    path('<int:pk>/products', views.ProductListAPI.as_view()),
]