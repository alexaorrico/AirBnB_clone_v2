#!/usr/bin/python3
""" app folder for API"""
from models import storage
from flask import Flask, Blueprint
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
HOST = getenv('HBNB_API_HOST', '0.0.0.0')
PORT = getenv('HBNB_API_PORT', '5000')


@app.teardown_appcontext
def teardown_storage(self):
    """closes storage if it exist"""
    if Storage is not None:
        storage.close()


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, threaded=True)
