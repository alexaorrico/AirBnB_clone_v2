#!/usr/bin/python3

"""importation of libraries and modules """
from flask import Flask
import os
from models import storage
from api.v1.views import app_views

"""Instantiate a flask app by calling the Flask class"""
app = Flask(__name__)
app.register_blueprint(app_views)

def close_storage(exception=None):
    """method to handle app context storage"""
    storage.close()

"""Register the teardown function"""
app.teardown_appcontext(close_storage)

if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))

    app.run(host=host, port=port, debug=True, threaded=True)
