#!/usr/bin/python3
"""starting a Flask application"""

from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

@app.teardown_appcontext
def storage_close(Exception):
    """Closes storage"""
    storage.close()

if __name__ == '__main__':
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
