#!/usr/bin/python3
"""
    V1 App creation module
"""

import os
from flask_cors import CORS
from flask import Flask, jsonify

from models import storage
from api.v1.views import app_views


app = Flask(__name__)

# Creating a CORS instance allowing: /* for 0.0.0.0
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

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
    js = {"error": "Not found"}
    return jsonify(js), 404


if __name__ == '__main__':
    """
        run main flask web app
    """
    # get IP address and Port number from input
    # if no found, work with default values
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)

    # run app session
    app.run(threaded=True, host=host, port=port)
