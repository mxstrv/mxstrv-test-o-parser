FROM python:3.11.1-alpine

WORKDIR /telegram_bot

COPY requirements.txt .

ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python", "start.py"]