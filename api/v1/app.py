#!/usr/bin/python3
""" This file defines the Flask application for the Airbnb clone API."""

from os import getenv
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views

app = Flask(__name__)  

# register blueprints
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_app(exception):
    """Handles teardown"""  
    storage.close()  

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", default="0.0.0.0")
    port = getenv("HBNB_API_PORT", default=5000)
    app.run(host, port, debug=True, threaded=True)
