#!/usr/bin/python3
"""following directions"""
from api.v1.views import app_views
from flask import jsonify, Blueprint, render_template, abort


@app_views.route('/status', method['GET'])
def status():
    """status"""
    return (jsonify({'status':'OK'}))
