#!/usr/bin/python3
"""app for registering blueprint and starting flask"""

from os import getenv
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tearDown(self):
    """close query after each session"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """Customized error code
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", "5000")), threaded=True)
