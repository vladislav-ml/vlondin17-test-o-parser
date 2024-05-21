from django.urls import path

from .views import ListProductView, ProductView

urlpatterns = [
    path('products/<int:pk>/', ProductView.as_view(), name='api_product'),
    path('products/', ListProductView.as_view(), name='api_list'),
]
