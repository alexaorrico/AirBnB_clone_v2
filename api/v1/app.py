#!/usr/bin/python3
"""
  Flask App integrated with AirBnB static 
"""
from flask import Flask, Blueprint, abort, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown(exception=None):
    """Close the current storage session"""
    storage.close()

if __name__ == "__main__":
    h = getenv('HBNB_API_HOST')
    p = getenv('HBNB_API_PORT')
    app.run(host=h, port=p, threaded=True)
