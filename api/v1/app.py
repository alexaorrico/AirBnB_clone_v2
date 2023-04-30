#!/usr/bin/python3
"""

Flask web server creation to handle api petition-requests

"""
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
CORS(app, origins="0.0.0.0")
api_host = getenv('HBNB_API_HOST', "0.0.0.0")
api_port = getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def teardown(self):
    """
    Commit changes in database
    """
    storage.close()


@app.errorhandler(404)
def Error_Handler(error):
    """
    The Error handler method is to hide a web page or an item from a user
    it also serve to redirect a user back to the main page
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=api_host, port=int(api_port), threaded=True)
