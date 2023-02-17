#!/usr/bin/python3
"""App views and route defined"""
from api.v1.views import app_views
from flask import Flask, , request, jsonify


@app.route('/status', methods=['GET'])
def status():
    """Show the status"""
    if request.method == 'GET':
        response = {"status": "OK"}
        return jsonify(response)
