#!/usr/bin/python3
"""This module contain a web application for the airbnb
    website
"""
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(exception):
    """close the session after every request"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ the function is called when a page is not found """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """ Execute the following line if not imported """
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
