#!/usr/bin/python3
"""Module contains views (route) for status"""
from api.v1.views import app_views
from flask import Flask, jsonify


app = Flask(__name__)


@app_views.route('/status', strict_slashes=False)
def status():
        """Endpoint to check the status of the API"""
        return jsonify({"status": "OK"})
