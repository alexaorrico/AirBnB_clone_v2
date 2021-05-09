#!/usr/bin/python3
""" Status of your API """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def app_status():
    '''
    Returns the Status of the API
    '''
    return(jsonify(status="OK"))
