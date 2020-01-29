#!/usr/bin/python3
"""
Returns the status of the API
"""

import models
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


HOST = getenv('HBNB_API_HOST', "0.0.0.0")
PORT = getenv('HBNB_API_PORT', 5000)

app = Flask(__name__)
# registers the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exe):
    """closes storage"""
    storage.close()


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, threaded=True)
