#!/usr/bin/python3
""" start a flask application """

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
import json
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(ret):
    """ call storage.close method """
    storage.close()


@app.errorhandler(404)
def get_nop(e):
    """handler for 404 errors"""
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
