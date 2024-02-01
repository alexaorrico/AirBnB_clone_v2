#!/usr/bin/python3

from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
import environ

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext()
def teardown_db(self):
    """teardown db"""
    storage.close()


if __name__ == "__main__":
    app.run(
        host=environ.getenv(
            'HBNB_API_HOST',
            '0.0.0.0'),
        port=environ.getenv(
            'HBNB_API_PORT',
            '5000'),
        threaded=True)
