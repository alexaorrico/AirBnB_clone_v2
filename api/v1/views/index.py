#!/usr/bin/python3
"""
Script that starts a Flask web application
"""
from flask import Flask, jsonify
#from api.v1.views import app_views

app_views = Flask(__name__)


@app_views.route("/status", methods=("GET"))
def status():
    """ Returns a JSON: "status": "OK"""
    return jsonify({"status": "OK"})
