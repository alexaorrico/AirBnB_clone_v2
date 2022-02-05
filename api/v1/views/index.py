#!/usr/bin/python3
""""""
from api.v1.views import app_views
from flask import Flask, jsonify
app = Flask(__name__)


@app_views.route('/status', strict_slashes=False)
def index():
    return jsonify({"status": "OK"})
