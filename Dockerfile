FROM python:3.10-slim

WORKDIR /hotelbot

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "main.py"]