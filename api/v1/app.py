#!/usr/bin/python3

"""
Flask App
"""

from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    closes the database connection
    """
    storage.close()


if __name__ == "__main__":
    """
    Runs the flask application
    """
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    app.run(host=host, port=port, threaded=True)
