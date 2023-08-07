from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE

from api.serializers import ProductSerializer, ProductPOSTSerializer
from core.tasks import parse_and_add_to_db, proxy_accessible_check
from products.models import Product


@swagger_auto_schema(
    method='GET',
    query_serializer=ProductSerializer(many=True),
    responses={200: "Данные о товарах получены"},
    operation_description='Получение данных о товарах из базы данных'
)
@swagger_auto_schema(
    method='POST',
    query_serializer=ProductPOSTSerializer(),
    responses={200: "Задача для старта парсинга отправлена",
               503: "Прокси сервер не отвечает",
               },
    operation_description='Отправка запроса на парсинг данных с Ozon'
)
@api_view(['GET', 'POST'])
def products_view(request):
    if request.method == 'POST':
        serializer = ProductPOSTSerializer(data=request.data)
        if serializer.is_valid():
            products_count = serializer.validated_data.get('products_count')
            parse_and_add_to_db.delay(products_count)
            if not proxy_accessible_check():
                return Response('Прокси сервер недоступен',
                                status=HTTP_503_SERVICE_UNAVAILABLE)
            return Response('Процесс парсинга начался', status=HTTP_200_OK)

    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=HTTP_200_OK)


@swagger_auto_schema(
    method='GET',
    query_serializer=ProductSerializer(),
    responses={200: "Данные о товаре получены"},
    operation_description='Получение данных о товаре по product_id из БД'
)
@api_view(['GET'])
def get_product_by_id(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    serializer = ProductSerializer(product)
    return Response(serializer.data, status=HTTP_200_OK)
