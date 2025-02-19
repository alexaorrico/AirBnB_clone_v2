#!/usr/bin/python3
"""Creating Index page"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def api_status():
    """
       app index function
    """
    response = {'status': 'OK'}
    return jsonify(response)
