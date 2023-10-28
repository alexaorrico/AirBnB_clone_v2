#!/usr/bin/python3
""""""

from api.v1.views import app_views, jsonify


@app_views.route("/status")
def status():
    """"""
    data = {
        'status': 'OK'
    }
    return (jsonify(data))
