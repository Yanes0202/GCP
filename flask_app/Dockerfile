# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

# Ustawienie katalogu roboczego na poziomie aplikacji
WORKDIR /flask_app

# Kopiowanie pliku requirements.txt i instalowanie zależności
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Kopiowanie reszty aplikacji do kontenera
COPY . .

# Ustawienie punktu wejścia dla kontenera na run.py
CMD ["python3", "run.py"]
