#!/usr/bin/python3
"""
Index allots a port and access for
Blueprint to run
"""


from flask import Flask
from api.v1.views import app_views


@app.route('/status', strict_slashes=False)
def app_views():
    """return jsonificated version of 'status:ok'"""
    return flask.jsonify(response_value_1="status",
                         response_value_2="OK")
