#!/usr/bin/python3
"""return json object"""


from flask import Flask, jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """Return json with status"""
    ret = {"status": "OK"}
    return jsonify(ret)
