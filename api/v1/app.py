#!/usr/bin/python3
"""
Starts a flask application
"""
import os

from api.v1.views import app_views
from flask import Flask
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exc):
    """
    method that calls storage.close()
    """
    storage.close()


if __name__ == "__main__":
    app_host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    app_port = int(os.getenv("HBNB_API_PORT", "5000"))
    app.run(host=app_host, port=app_port, threaded=True)
