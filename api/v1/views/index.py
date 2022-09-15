#!/usr/bin/python3
"""return json object"""




@app_views.route('/status')
def status():
    from flask import Flask, jsonify
    from api.v1.views import app_views
    """Return json with status"""
    ret = {"status": "OK"}
    return jsonify(ret)
