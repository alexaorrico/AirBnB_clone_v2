#!/usr/bin/python3
"""Status of your API"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """calls storage.close()"""
    storage.close()


@app.errorhandler(404)
def error_handler(not_found):
    """“404 page”, a “Not found”"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    HBNB_API_HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    HBNB_API_PORT = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
