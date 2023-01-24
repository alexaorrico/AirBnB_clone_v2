#!/usr/bin/python3
"""Script to return the status of an API"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views, url_prefix="/api/v1")
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def error_page(error):
    """Return error page if specified page is unreachable"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_db(self):
    """tear down db"""
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else '0.0.0.0'
    port = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else 5000
    app.run(host=host, port=port, threaded=True)
