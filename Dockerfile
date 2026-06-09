FROM python:3.12-slim

WORKDIR /gamebot

COPY ./main.py .
COPY ./partida.py .
COPY ./tablero.py .
COPY ./requirements.txt .
COPY ./globales.py .

RUN apt-get update && apt-get install -y python3-pip && pip install --upgrade pip && pip install -r "requirements.txt"

CMD ["python", "main.py"]
