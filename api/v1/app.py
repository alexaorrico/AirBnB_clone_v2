#!/usr/bin/python3
"""Script to return the status of an API"""

from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.errorhandler(404)
def error_page(error):
    """Return error page if specified page is unreachable"""
    return jsonify({"error": "Not found"})


@app.teardown_appcontext
def teardown_db(self):
    """tear down db"""
    storage.close()


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST') or '0.0.0.0',
            port=getenv('HBNB_API_HOST') or 5000, threaded=True)
