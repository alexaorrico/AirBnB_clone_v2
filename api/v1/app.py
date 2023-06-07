#!/usr/bin/python3
"""Api v1 for AirBnB clone"""

from models import storage
from flask import Flask
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")

@app.teardown_appcontext
def close_app(exc):
    """Closes storage engine"""
    storage.close


if __name__ == "__main__":
    host = "0.0.0.0"
    post = "5001"
    if os.environ.get('HBNB_API_HOST'):
        host = os.environ.get('HBNB_API_HOST')
    if os.environ.get('HBNB_API_PORT'):
        port = os.environ.get('HBNB_API_PORT')
    app.run(host=host, port=port, threaded=True)
