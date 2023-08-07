from django.db import models


class Product(models.Model):
    """Модель для структурирования информации с
    маркетплейса.
    """
    product_id = models.IntegerField(
        'id товара на ozon',
        blank=False,
        null=False,

    )
    name = models.CharField(
        'название товара',
        blank=False,
        max_length=500,
    )
    price = models.IntegerField(
        'цена товара'
    )
    rating = models.FloatField(
        'рейтинг товара'
    )
    comments = models.IntegerField(
        'количество комментариев'
    )
    discount = models.CharField(
        'скидка на товар',
        max_length=5
    )
    image_url = models.CharField(
        'ссылка на изображение',
        max_length=500
    )
    added_at = models.DateTimeField(
        'Дата добавления товара',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Товар Ozon'
        verbose_name_plural = 'Товары Ozon'
