#!/usr/bin/python3
""" HBNB flask application """

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def clean(exception=None):
    """ close storage sessions """
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """handle 404 error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host, port, threaded=True)
