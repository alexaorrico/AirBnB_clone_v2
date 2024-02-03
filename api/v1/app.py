#!/usr/bin/python3
"""Flask App"""


from api.v1.views import app_views
from flask import Flask
from os import environ
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown_db(exception=None):
    """Closes storage on teardown"""
    storage.close()


if __name__ == "__main__":
    if environ.get('HBNB_API_HOST'):
        HBNB_HOST = environ.get('HBNB_API_HOST')
    else:
        HBNB_HOST = '0.0.0.0'

    if environ.get('HBNB_API_HOST'):
        HBNB_PORT = environ.get('HBNB_API_PORT')
    else:
        HBNB_PORT = '5000'
    app.run(host=HBNB_HOST, port=HBNB_PORT, debug=True)
