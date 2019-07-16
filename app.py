"""
Single-endpoint app that takes a blob name and serves it up from the
configured GCP bucket. The assumption is that this sits behind an
nginx auth_request.
"""
from flask import Flask, Response, abort
from google.cloud import storage
import logging
import os
DEFAULT_BUCKET = 'uwit-iam-identity-artifacts'


def configure_logging():
    gunicorn_logger = logging.getLogger('gunicorn.error')
    level = logging.DEBUG
    if gunicorn_logger:
        level = gunicorn_logger.level
    logging.getLogger().setLevel(level)


configure_logging()
app = Flask(__name__)


@app.route('/')
def index():
    """Health check."""
    storage.Client()
    return 'all good'


@app.route('/<path:path>')
def proxy(path):
    """Return the contents of the given path."""
    app.logger.info(f'getting {path}')
    bucket_name = os.environ.get('GOOGLE_STORAGE_BUCKET', DEFAULT_BUCKET)
    bucket = storage.Client().bucket(bucket_name)
    if path.endswith('/'):
        path += 'index.html'
    blob = bucket.get_blob(path)
    if not blob:
        app.logger.error(f'not found: {path}')
        abort(404)
    return Response(blob.download_as_string(), mimetype=blob.content_type)
