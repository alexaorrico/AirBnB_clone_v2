#!/usr/bin/python3
"""
views for home/index page
"""
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views

@app_views.route('/status', strict_slashes=False)
def hbnbStatus():
    """hbnbStatus"""
    return jsonify({"status": "OK"})