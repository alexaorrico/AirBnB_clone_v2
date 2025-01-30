#!/usr/bin/python3
"""main app of API"""
from flask import Flask
from flask import abort
from flask import make_response
from flask import jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)

api_host = os.getenv("HBNB_API_HOST", default='0.0.0.0')
api_port = os.getenv("HBNB_API_PORT", default=5000)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """close storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """a handler for 404 errors that returns a
    JSON-formatted 404 status code response.
    """
    return make_response(jsonify({"error": "Not found"}), 400)


if __name__ == "__main__":
    app.run(host=api_host, port=api_port, threaded=True, debug=True)
