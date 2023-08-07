FROM python:3.11.1-alpine

WORKDIR /app

COPY requirements.txt .

RUN apt-get update
RUN apt -y install default-libmysqlclient-dev build-essential
RUN pip install --upgrade pip
RUN pip install gunicorn==20.1.0
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ozon_parser.wsgi"]