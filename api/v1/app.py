#!/usr/bin/python3
"""Flask app file v1"""

from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from os import environ


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views, url="/app_views")


@app.teardown_appcontext
def teardown(exception):
    """calls storage.close"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ returns 404 template on 404 code status """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(environ.get('HBNB_API_PORT', 5000))
    app.register_error_handler(404, page_not_found)
    app.run(
        host=host,
        port=port,
        threaded=True)
