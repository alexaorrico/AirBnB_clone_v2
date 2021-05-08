#!/usr/bin/python3
""" create a variable app_views which is an instance of Blueprint """
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """ this might be broken """
    return ({'"status": "OK"'})
