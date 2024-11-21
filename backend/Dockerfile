FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=backend.settings

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/

CMD python manage.py makemigrations api channel && \
    python manage.py migrate && \
    python manage.py adminuser_token --no-input && \
    python manage.py collectstatic --noinput && \
    daphne backend.asgi:application --port 8000 --bind 0.0.0.0