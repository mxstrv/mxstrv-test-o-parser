import requests
from bs4 import BeautifulSoup
from celery import shared_task

from products.models import Product


MARKETPLACE_URL = 'https://ozon.ru/seller/1/products'


def parse_page(page: str) -> str:
    """Функция для парсинга html страницы по ссылке.

    Для обхода защиты Cloudflare используется прокси сервер
    из docker-контейнера, представляющий собой headless браузер
    на базе Chromium с undetectable драйвером.

    :param page: URL сайта.
    :type page: str

    :return: HTML текст для дальнейшего парсинга.
    :rtype: str

    :raise requests.exceptions.ConnectionError
        Если прокси сервер отдает код, отличный от 200.
    """

    post_body = {
        "cmd": "request.get",
        "url": page,
        "maxTimeout": 60000
    }

    response = requests.post(
        # POST запрос на прокси сервер
        'http://flaresolverr:8191/v1',
        headers={'Content-Type': 'application/json'},
        json=post_body
    )

    if response.status_code == 200:
        return response.json()["solution"]["response"]
    else:
        raise requests.exceptions.ConnectionError(
            f"Прокси сервер выдал {response.status_code}")


def scrape_page_products(html_content: str, limit_number: int) -> list[dict]:
    """Функция парсит содержимое карточек товаров на странице и
    возвращает массив со словарями для дальнейшего превращения
    его в Django QuerySet и добавление в БД.

    :param html_content: HTML Содержимое страницы.
    :type html_content: str

    :param limit_number: Условие для выхода из цикла, если товаров
    в возврате функции нужно меньше, чем имеется на странице.
    :type limit_number: int

    :return: Массив словарей с товарами и их характеристиками.
    :rtype: list[dict]
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    elements_grid = soup.find('div',
                              class_='widget-search-result-container'
                              ).find('div')
    target_elements = elements_grid.find_all('div', recursive=False)
    result = []

    for element in target_elements:

        product_url = element.find(
            'a', class_='tile-hover-target')['href'].split('/')[2]
        product_id = int(product_url.split('-')[-1])

        name = element.find('span', class_='tsBody500Medium').text

        price = element.find(
            'span', class_='tsHeadline500Medium').text
        formatted_price = int(price.replace(" ", "").replace("₽", "").strip())

        discount = element.find_all(
            'span', class_='tsBodyControl400Small')[1].text

        try:
            rating, comments = element.find(
                'div', class_='tsBodyMBold').text.split('  ')
        except AttributeError:
            rating, comments = str(0), str(0)

        image_url = element.find(
            'div').find('img')['srcset'].split(' ')[0]

        result.append({
            'product_id': product_id,
            'name': name,
            'price': formatted_price,
            'rating': rating,
            'comments': comments,
            'discount': discount,
            'image_url': image_url
        })

        if len(result) == limit_number:
            return result

    return result


@shared_task()
def parse_and_add_to_db(number: int) -> None:
    """Функция, отвечающая за парсинг данных и добавление данных в
    БД.

    :param number: Ограничитель количества товаров из POST-запроса.
        По-умолчанию равен 10.
    :type number: int
    """
    products_result = []
    page_num = 1
    current_n = number
    while len(products_result) < number:
        page_content = parse_page(MARKETPLACE_URL + f'?page={page_num}')
        products_result.extend(scrape_page_products(page_content, current_n))
        page_num += 1
        current_n -= len(products_result)

    for item in products_result:
        product_id = item['product_id']
        try:
            product = Product.objects.get(product_id=product_id)
            for key, value in item.items():
                setattr(product, key, value)
            product.save()
        except Product.DoesNotExist:
            product = Product(**item)
            product.save()


def proxy_accessible_check() -> bool:
    """Функция для проверки доступности прокси сервера.

    :returns: Возвращает False, если прокси сервер
    недоступен
    """
    try:
        request = requests.get('http://flaresolverr:8191')
        return True if request.status_code == 200 else False
    except requests.exceptions.ConnectionError:
        return False
