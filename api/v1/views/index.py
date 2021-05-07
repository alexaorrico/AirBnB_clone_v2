#!/usr/bin/python3
""" create a variable app_views which is an instance of Blueprint """
from api.v1.views import app_views


@app.route("/status")
def app_views():
    """ this might be broken """
    return '"status": "OK"'
