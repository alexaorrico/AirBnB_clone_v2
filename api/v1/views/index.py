#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from v1.app import app

@app.route("/status")
def app_views():
    """return the status"""
    return jsonify({"status": "OK"})
