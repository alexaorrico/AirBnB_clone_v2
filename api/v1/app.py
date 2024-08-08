#!/usr/bin/python3
"""Flask app main module"""


from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def shutdown(exception=None):
    """close storage after every request"""
    storage.close()


@app.errorhandler(404)
def handle_not_found(error):
    """return a not found response"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    HBNB_API_HOST = "0.0.0.0"
    HBNB_API_PORT = 5000

    if getenv("HBNB_API_HOST"):
        HBNB_API_HOST = getenv("HBNB_API_HOST")

    if getenv("HBNB_API_PORT"):
        HBNB_API_PORT = getenv("HBNB_API_PORT")

    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
