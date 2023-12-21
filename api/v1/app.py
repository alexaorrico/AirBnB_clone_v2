#!/usr/bin/python3
""" Module for app.py """

from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify
from flask import Blueprint
from os import getenv

# Create Flask app
app = Flask(__name__)

# Create blueprint
app.register_blueprint(app_views)


# Declare method to handle @app.teardown that calls storage.close
@app.teardown_appcontext
def teardown_db(exception):
    """ Method to close storage """
    storage.close()


# Declare method to handle 404 errors
@app.errorhandler(404)
def not_found(error):
    """ Method to handle 404 error """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """Main method"""""
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
