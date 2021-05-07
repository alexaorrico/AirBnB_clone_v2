#!/usr/bin/python3
from api.v1.views import app_views


@app.route("/status")
def app_views():
    """ this might be broken """
    return '"status": "OK"'
