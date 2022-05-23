FROM python:3.9.13-slim

ENV MONGO_HOST mongodb
ENV MONGO_DB development

COPY ./src /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD python app.py
