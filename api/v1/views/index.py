#!/usr/bin/python3
"""
index page for flask
displays status
"""
from flask import Flask, jsonify
from api.v1.views import app_views


@app_views.route('/status')
def get_status():
    return jsonify({"status": "OK"})