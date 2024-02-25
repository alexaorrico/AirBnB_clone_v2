#!/usr/bin/python3
"""
    This module creates an api endpoint
"""

from api.v1.views import app_views
from flask import Flask
from flask import jsonify
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


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error="Not found")


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else '0.0.0.0'
    port = int(getenv('HBNB_API_PORT')) if getenv('HBNB_API_PORT') else 5000
    app.run(host=host, port=port, threaded=True)
