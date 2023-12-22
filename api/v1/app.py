#!/usr/bin/python3
"""module for app file of hbnb clone"""
from api.v1.views import app_views
from flask import Flask
from models import storage
from flask import jsonify
from flask import Blueprint
import os


# set up app_views blueprint and flask instance
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """close storage session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
