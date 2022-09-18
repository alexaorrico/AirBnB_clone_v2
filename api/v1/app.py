#!/usr/bin/python3
"""script that starts a Flask web application"""

from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint
app.register_blueprint(app_views)

app = Flask(__name__)


@app.teardown_appcontext
def app_teardown(self):
    """method that calls storage.close()"""
    storage.close()

if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST") or '0.0.0.0',
    port=getenv("HBNB_API_PORT") or 5000,
    threaded=True)
