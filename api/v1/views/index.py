#!/usr/bin/python3
from api.v1.views import app_views
import jsonify


@app_views.route('/status')
def status():
    """
    returns an OK Jsonified
    """
    return jsonify({"status": "OK"})


@app_view.route('/api/v1/stats')
def _counts():
    """
    retrieves the number of each objects per type
    """
	
