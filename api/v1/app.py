#!/usr/bin/python3
""""
This module contains the principal application
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(obj):
    """ calls methods close() """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Loads a custom 404 page not found"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)

    app.run(host, int(port), threaded=True)
