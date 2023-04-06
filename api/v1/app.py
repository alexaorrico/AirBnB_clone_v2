#!/usr/bin/python3
"""Module"""
from flask import Flask, render_template, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(self):
    """calls storage.close()"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """error handler for page not found"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"), port=int(
        getenv("HBNB_API_PORT", "5000")), threaded=True)