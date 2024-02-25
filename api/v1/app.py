#!/usr/bin/python3
"""
    This module creates an api endpoint
"""

from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear(self):
    """
        Closes the storage
    """
    storage.close()


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else '0.0.0.0'
    port = int(getenv('HBNB_API_PORT')) if getenv('HBNB_API_PORT') else 5000
    app.run(host=host, port=port, threaded=True)
