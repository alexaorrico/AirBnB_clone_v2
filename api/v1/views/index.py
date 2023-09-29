#!/usr/bin/python3
from flask import Flask, jsonify
from api.v1.views import app_views


@app.route('/status')
def return_status(app_views):
    """Return status code"""
    response = jsonify(app_views)
    return response['status']
