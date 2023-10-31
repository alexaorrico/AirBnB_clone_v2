#!/usr/bin/python3

from api.v1.views import app_views
from flask import Flask, jsonify

@app_views.route('status')
def return_status():
    """ returns a json response """
    status = {"status": "OK"}
    return jsonify(status)
