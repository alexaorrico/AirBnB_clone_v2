#!/usr/bin/python3
""" creating the first api"""
from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext('storage_close')
def storage_close():
    """
    The decorator call the storage.close method
    """
    storage.close()


if __name__ == "__main__":
    # Retrieve host and port from env variables or use defaults
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", 5000))

    # Runs the app instance with port and host
    app.run(host=host, port=port, threaded=True)

