FROM python:3.10-alpine

WORKDIR /api

COPY ./requirements.txt .

RUN apk update && apk add g++

RUN apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev && \
    apk add --no-cache libffi-dev libressl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

RUN pip install uvicorn

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]