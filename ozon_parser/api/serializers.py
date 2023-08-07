from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для GET запросов.
    """
    class Meta:
        model = Product
        fields = '__all__'


class ProductPOSTSerializer(serializers.Serializer):
    """Сериализатор для POST запросов для старта парсинга товаров.
    """
    products_count = serializers.IntegerField(
        default=10,
        min_value=1,
        max_value=50
    )
