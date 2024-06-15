# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

# Ustawienie katalogu roboczego na poziomie aplikacji
WORKDIR /bucket_app

# Kopiowanie pliku requirements.txt i instalowanie zależności
COPY bucket_app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Kopiowanie reszty aplikacji do kontenera (tylko folderu bucket_app)
COPY bucket_app/ .

# Ustawienie punktu wejścia dla kontenera na bucket.py
CMD ["python3", "bucket.py"]