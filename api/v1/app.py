#!/usr/bin/python3
"""script returns the status of our API"""
import os

from flask import Flask

from api.v1.views import app_views
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(exception):
    """handles the teardown context"""
    storage.close()


if __name__ == "__main__":
    HOST = os.getenv("HBNB_API_HOST", "0.0.0.0")
    PORT = os.getenv("HBNB_API_PORT", "5000")

    app.run(host=HOST, port=PORT, threaded=True)
