#!/usr/bin/python3
""" app.py """

from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(dummy):
    """ closes after being run """
    storage.close()


if __name__ == "__main__":

    from os import getenv

    host = getenv('HBNB_API_HOST')
    if host is None:
        host = '0.0.0.0'

    port = getenv('HBNB_API_PORT')
    if port is None:
        port = 5000

    app.run(
        host=host,
        port=port,
        threaded=True,
        debug=True
    )
