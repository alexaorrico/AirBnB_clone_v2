#!/usr/bin/python3

"""Status of API"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(exception):
    """Closes session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """page not found"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """Runs app on in this module"""
    app.run(host=os.getenv("HBNB_API_HOST", "0.0.0.0"), port=os.getenv(
            "HBNB_API_PORT", "5000"), threaded=True)
