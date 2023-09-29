"""Defines the status route for our API"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """Returns JSON response for status OK """
    return jsonify({'status': 'OK'})
