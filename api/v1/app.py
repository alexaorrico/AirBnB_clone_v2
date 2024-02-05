#!/usr/bin/python3
"""This module contain a flask web application framework
    for the airbnb website

    It contains two functions
"""
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_session(exception):
    """close the session after every request"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ the function is called when a page is not found """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """Execute the following line if not imported"""
    HOST = os.getenv("HBNB_API_HOST", "0.0.0.0")
    PORT = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=HOST, port=PORT, threaded=True)
