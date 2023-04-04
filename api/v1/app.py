#!/usr/bin/python3
"""
Sets up first endpoint that returns stats of the API
"""

from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from models import storage
from os import getenv


app = Flask(__name__)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    Calls storage.close
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    """
    404 Page Not Found Error Handler
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = "0.0.0.0"
    port = "5000"
    if getenv("HBNB_API_HOST"):
        host = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT"):
        port = getenv("HBNB_API_PORT")

    app.run(host=host, port=port, threaded=True)
