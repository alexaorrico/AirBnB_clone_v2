"""Module with routes for app_views blueprint"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """Returns a json with status ok"""
    return jsonify({'status': 'OK'})
