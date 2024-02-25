#!/usr/bin/python3
""" Application file API
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardownSession(expection):
    """Closes session"""
    storage.close()


@app.errorhandler(404)
def handle_404_error(_error):
    resp = jsonify({"error": "Not found"})
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
