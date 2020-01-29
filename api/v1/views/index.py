#!/usr/bin/python3
""" create a route status that returns  a JSON """


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """ return JSON object """
    return jsonify(
        {
            "status": "OK"
        })
