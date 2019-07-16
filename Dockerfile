FROM python:3-slim

RUN pip install -U google-cloud-storage flask gunicorn[eventlet]

COPY . /app

ENV GOOGLE_APPLICATION_CREDENTIALS=/etc/gcloud/key.json \
    FLASK_APP=app.py

WORKDIR /app
COPY . /app

CMD ["gunicorn", "--worker-class", "eventlet", "--bind", ":5000", "app:app"]
