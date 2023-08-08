FROM python:3.11.1

WORKDIR /app

COPY requirements.txt .

ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN pip install gunicorn==20.1.0
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN python manage.py collectstatic --no-input

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ozon_parser.wsgi"]