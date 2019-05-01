#!/usr/bin/python3
"""Flask app file v1"""

from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from os import environ


app = Flask(__name__)
app.register_blueprint(app_views, url="/app_views")

@app.teardown_appcontext
def teardown():
    """calls storage.close"""
    storage.close()


if __name__ == "__main__":
    app.run(
        host=environ.get(HBNB_API_HOST),
        port=environ.get(HBNB_API_PORT),
        threaded=True)
