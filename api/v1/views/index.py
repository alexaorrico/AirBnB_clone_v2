#!/usr/bin/python3
""" index module """


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """ return status of api """
    return jsonify({
            "status": "Ok"
        })
