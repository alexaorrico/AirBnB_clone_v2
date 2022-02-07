#!/usr/bin/python3
"""
API module
"""

from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext  # Application context
def teardown(exception):
    """ Call storage.close() """
    storage.close()


if __name__ == '__main__':

    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')

    if not host:
        host = "0.0.0.0"  # Default host
    if not port:
        port = "5000"  # Default port

    app.run(host, port, threaded=True)
