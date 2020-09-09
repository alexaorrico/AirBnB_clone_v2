#!/usr/bin/python3
"""Starts a Flask API application."""
import os
from models import storage
from api.v1.views import app_views, index
from flask import Flask, jsonify

app = Flask(__name__)


@app.teardown_appcontext
def close_funtion(self):
    """close funtion."""
    storage.close()


@app.route('/', strict_slashes=False)
def index():
    """returns Hello HBNB!"""
    return 'Hello HBNB! ESTEBAN'

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return jsonify({ "error": "Not found"}), 404


app.register_blueprint(app_views)



if __name__ == '__main__':
    app.run(host=os.environ.get('HBNB_API_HOST'),
            port=os.environ.get('HBNB_API_PORT'), debug=True)
