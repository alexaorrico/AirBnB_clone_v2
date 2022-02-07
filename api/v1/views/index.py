#!/usr/bin/python3
""" Status """

from api.v1.views import app_views


@app_views.route('/status')
def status():
    """ Status of API """
    return jsonify({"status": "OK"})
