#!/usr/bin/python3
"""Create a flask application for the API"""

from os import getenv

from flask import Flask

from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(eexception):
    """Closes the storage"""
    storage.close()


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", '0.0.0.0'),
            port=getenv("HBNB_API_PORT", '5000'),
            threaded=True)
