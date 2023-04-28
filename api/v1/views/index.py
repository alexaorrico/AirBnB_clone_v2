from . import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Status route to returns the status of the API"""
    return jsonify({'status': 'ok'})


@app_views.route('/stats')
def status():
    # implement count and return
    return jsonify({'status': 'ok'})
