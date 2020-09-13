FROM python:3.8 as builder

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry lock
RUN poetry export -f requirements.txt --without-hashes --dev > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY docker-entrypoint.sh .
ENTRYPOINT ["./docker-entrypoint.sh"]
COPY .. .
EXPOSE 80

FROM python:3.8

WORKDIR /app

COPY --from=builder /app/requirements.txt .

RUN set -ex \
  && pip install --no-cache-dir -r requirements.txt

COPY docker-entrypoint.sh .
ENTRYPOINT ["./docker-entrypoint.sh"]
COPY .. .