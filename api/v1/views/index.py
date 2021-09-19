#!/usr/bin/python3
'''
    Returns the status of the API
'''


from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def index():
    return jsonify({'status': 'OK'})
