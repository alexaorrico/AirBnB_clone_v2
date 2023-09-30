#!/usr/bin/python3
"""
    V1 App creation module
"""

import os
from flask import Flask, jsonify
from markupsafe import escape

from models import storage
from api.v1.views import app_views


app = Flask(__name__)

#  register a blueprint 'app_views'
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_db(exception):
    """
        Close SQL Alchemy session after each request made
    """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """
        a handler for 404 errors that returns a JSON-formatted
        404 status code response
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    """
        run main flask web app
    """
    # get IP adress and Port number from input
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)

    # run app session
    app.run(threaded=True, host=host, port=port)
