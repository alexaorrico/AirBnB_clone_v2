#!/usr/bin/python3
"""This is an api version 1 module."""
from flask import Flask, make_response, jsonify
from models import storage
import os
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.url_map.strict_slahes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """close all storage connections at the end of the reques."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors by returning a JSON response"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(
        host=os.getenv("HBNB_API_HOST") if os.getenv(
            "HBNB_API_HOST") else "0.0.0.0",
        port=os.getenv("HBNB_API_PORT") if os.getenv(
            "HBNB_API_PORT") else "5000",
        threaded=True
    )
