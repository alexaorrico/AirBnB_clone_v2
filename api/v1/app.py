#!/usr/bin/python3
"""
script To return the status of API
"""

from api.v1.views import app_views
from flask import Flask
from models import *
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = int(getenv('HBNB_API_PORT', default=5000))

    app.run(host, port, threaded=True)
