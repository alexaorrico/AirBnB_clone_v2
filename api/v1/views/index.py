#!/usr/bin/python3
"""
Flask app
"""
from flask import Flask, render_template, jsonify
from api.v1.views import app_views

@app_views.route('/status', method={'GET'})
def status():
    """status"""
    return jsonify({"status": "OK"})
