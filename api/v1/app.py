#!/usr/bin/python3
"""
This is the app module
"""

from flask import Flask, jsonify
from os import getenv
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def session_close(exception):
    """
    This function close session
    """
    storage.close()

@app.errorhandler(404)
def wrong_route(e):
    """
    handles error 404
    """
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    app.run(
        host=getenv('HBNB_API_HOST') or '0.0.0.0',
        port=getenv('HBNB_API_PORT') or '5000',
        threaded=True
    )
