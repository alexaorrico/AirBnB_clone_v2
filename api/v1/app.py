#!/usr/bin/python3
""" This module defines the entry point for our Flask API"""

from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(error):
    """ Closes the storage """
    storage.close()


if __name__ == '__main__':
    """ Main Function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
