#!/usr/bin/python3
"""Module contains flask app"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def closeStorage(exception):
    """Closes the storage session"""
    storage.close()


if __name__ == '__main__':
    useHost = getenv('HBNB_API_HOST', default='0.0.0.0')
    usePort = getenv('HBNB_API_PORT', default=5000)

    app.run(host=useHost, port=usePort, threaded=True)
