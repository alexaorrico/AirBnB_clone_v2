#!/usr/bin/python3

from flask import Flask
from flask.globals import request
from flask.json import jsonify

from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})
