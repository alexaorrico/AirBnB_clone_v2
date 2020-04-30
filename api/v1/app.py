#!/usr/bin/python3
"""
"""

from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(self):
    """
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
