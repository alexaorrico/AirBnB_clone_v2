#!/usr/bin/python3
"""Status APi """"
from flask import Flask, jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """Status API by json file"""
    return jsonify({"status": "OK"})
