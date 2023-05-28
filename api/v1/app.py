#!/usr/bin/python3
""" Status of your API"""
import os
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
db = os.environ.get('HBNB_TYPE_STORAGE', 'json_file')
host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
port = os.environ.get('HBNB_API_PORT', '5000')
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resource={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close(cls):
    """close"""
    storage.close()


if __name__ == "__main__":
    """Initialize api"""
    app.run(host=host, port=int(port), threaded=True)
