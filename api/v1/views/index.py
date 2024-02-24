#!/usr/bin/python3
""" index file """

from api.v1.views import app_views

@app_views.route('/status', method=['GET'], strict_slashes=False)
def status():
    """ returns a JSON """
    return jsonify(status="OK")
