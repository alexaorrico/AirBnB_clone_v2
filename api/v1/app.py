#!/usr/bin/python3

"""
API status
"""

import os
from models import storage
from flask import Flask
from api.v1.views import app_views


app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """close storage"""
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
