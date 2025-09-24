from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SaleViewSet
from .pos_views import pos_quick_sale, pos_receipt, pos_product_search

router = DefaultRouter()
router.register(r'', SaleViewSet, basename='sales')

urlpatterns = [
    path('', include(router.urls)),
    # POS specific endpoints
    path('pos/quick-sale/', pos_quick_sale, name='pos-quick-sale'),
    path('pos/receipt/<uuid:sale_id>/', pos_receipt, name='pos-receipt'),
    path('pos/search-products/', pos_product_search, name='pos-product-search'),
]

