FROM python:3.10-slim

COPY . ./hotelbot

WORKDIR /hotelbot

RUN python -m pip install -r requirements.txt


ENTRYPOINT ["python", "main.py"]