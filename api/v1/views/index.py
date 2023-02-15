#!/usr/bin/python3
""" index for out api """

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', strict_slashes=False)
def status_route():
    """ Status of the web server"""
    return jsonify({"status": 'OK'})

if __name__ == '__main__':
    pass