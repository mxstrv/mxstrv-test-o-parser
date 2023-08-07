from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id',
                    'name',
                    'price',
                    'rating',
                    'comments',
                    'discount',
                    'image_url',
                    'added_at'
                    )
    list_filter = ('added_at',)
    search_fields = ('product_id', 'name')
