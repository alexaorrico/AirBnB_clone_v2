#!/usr/bin/python3
import json

from flask import jsonify

from api.v1.views import app_views


@app_views.route("/status")
def check_status():
    """ return status ok as json"""
    dict_ = { 'status' : "OK"}
    
    return jsonify(dict_)