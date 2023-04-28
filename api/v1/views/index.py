#!/usr/bin/python3
"""AirBnB clone API views"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """Returns a json object describing status"""
    return jsonify({'status': 'OK'})
