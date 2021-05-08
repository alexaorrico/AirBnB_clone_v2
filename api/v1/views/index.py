#!/usr/bin/python3
""" create a variable app_views which is an instance of Blueprint """
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """ returns status: OK """
    return ({'"status": "OK"'})

@app_views.route("api/v1/stats")
def stats():
    """ create endpoint that retrieves the number of eachobjects by type """
    return jsonify({storage.count()})
