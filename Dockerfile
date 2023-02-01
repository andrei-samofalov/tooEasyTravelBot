FROM python:3.10-slim

COPY . .

RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]