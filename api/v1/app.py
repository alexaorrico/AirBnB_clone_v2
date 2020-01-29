#!/usr/bin/python3
"""
Status of your API
"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def closer(self):
    """method that calls storage close"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """method that calls error pages"""
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
