from django.urls import path
from .views import *


urlpatterns = [
    # Category URLs
    path("cat/list/", ListCategory.as_view(), name="category-list"),
    path("cat/create/", CreateCategory.as_view(), name="category-create"),
    path("cat/update/<uuid:pk>/", UpdateCategory.as_view(), name="category-update"),
    path("cat/delete/<uuid:pk>/", DeleteCategory.as_view(), name="category-delete"),


    # Product URLs
    path("list/", ListProduct.as_view(), name="product-list"),
    path("create/", CreateProduct.as_view(), name="product-create"),
    path("detail/<uuid:pk>/", ProductDetail.as_view(), name="product-detail"),
    path("update/<uuid:pk>/", UpdateProduct.as_view(), name="product-update"),
    path("delete/<uuid:pk>/", DeleteProduct.as_view(), name="product-delete"),
    path("stock/<uuid:pk>/", UpdateProductStock.as_view(), name="update-product-stock"),
]
