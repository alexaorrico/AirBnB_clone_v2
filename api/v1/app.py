#!/usr/bin/python3
"""
initializing flask app
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views)

app.do_teardown_appcontext()


def tear_down(data):
    """
    tear down app
    """
    storage.close()


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', '5500')))