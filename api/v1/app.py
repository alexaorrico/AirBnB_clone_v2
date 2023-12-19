#!/usr/bin/python3
"""
start api
"""
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

app.register_blueprint(app_views)

def teardown_appcontext(exception):
    """Closes the storage on teardown."""
    storage.close()

app.teardown_appcontext(teardown_appcontext)

if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
