#!/usr/bin/python3
""" index """
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'])
def status():
    """ Returns the status of the request """
    return jsonify({'status': 'OK'})