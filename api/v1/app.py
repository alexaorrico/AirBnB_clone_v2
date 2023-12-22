#!/usr/bin/python3
"""module for app file of hbnb clone"""
from api.v1.views import app_views
from flask import Flask, render_template, make_response, jsonify
import os
from models import storage


# set up app_views blueprint and flask instance
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def not_found(error):
    """close storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return make_response(jsonifiy({"error": "Not found"}), 404)


if __name__ == "__main__":
    HBNB_API_HOST = os.getenv('HBNB_API_HOST', default='0.0.0.0')
    HBNB_API_PORT = os.getenv('HBNB_API_PORT', default='5000')
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
