#!/usr/bin/python3
"""Create a route on the object app_views that returns a JSON: "status":OK """
from api.v1.views import app_views
from flask import jsonify, Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

@app_views.route('/status', methods=['GET'])
def status():
    """Returns the status of the API"""
    return jsonify({'status': 'OK'})
