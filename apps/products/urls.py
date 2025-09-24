from django.urls import path
from .views import *


urlpatterns = [
    # Category URLs
    path("categories/", ListCategory.as_view(), name="category-list"),
    path("categories/", CreateCategory.as_view(), name="category-create"),
    path("categories/<uuid:pk>/", UpdateCategory.as_view(), name="category-update"),
    path("categories/<uuid:pk>/", DeleteCategory.as_view(), name="category-delete"),


    # Product URLs
    path("", ListProduct.as_view(), name="product-list"),
    path("", CreateProduct.as_view(), name="product-create"),
    path("<uuid:pk>/", ProductDetail.as_view(), name="product-detail"),
    path("<uuid:pk>/", UpdateProduct.as_view(), name="product-update"),
    path("<uuid:pk>/", DeleteProduct.as_view(), name="product-delete"),
    path("stock/<uuid:pk>/", UpdateProductStock.as_view(), name="update-product-stock"),
    
]
