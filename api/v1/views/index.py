#!/usr/bin/python3
"""Create a route that returns a JSON"""
from api.v1.views import app_views
from flask import Flask, jsonify

@app_views.route('/status')
def status():
    """returns json file"""
    return jsonify ({"status": "OK"})
