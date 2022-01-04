FROM ghcr.io/uwit-iam/poetry:latest AS dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install

ENV GOOGLE_APPLICATION_CREDENTIALS=/etc/gcloud/key.json \
    FLASK_APP=app.py

FROM dependencies

WORKDIR /app
COPY . /app

CMD ["gunicorn", "--worker-class", "gevent", "--bind", ":5000", "app:app"]
