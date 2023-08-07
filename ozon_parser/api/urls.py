from django.urls import path

from api.views import products_view, get_product_by_id

urlpatterns = [
    path('products/',
         products_view,
         name='products'),
    path('products/<int:product_id>',
         get_product_by_id,
         name='get_product_by_id')
]
