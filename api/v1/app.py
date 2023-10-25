#!/usr/bin/python3
"""AirBnB v3 flask Api v1 entrypoint"""
from os import environ
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


if __name__ == "__main__":
    """entrypoint"""
    flaskHost = environ.get('HBNB_API_HOST')
    flaskPort = environ.get('HBNB_API_PORT')
    if not flaskHost:
        flaskHost = '0.0.0.0'
    if not flaskPort:
        flaskPort = '5000'
    app.run(
        host=flaskHost,
        port=flaskPort,
        threaded=True
    )
