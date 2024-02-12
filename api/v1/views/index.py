#!/usr/bin/python3
"""index file"""
from flask import jsonify
from . import app_views

@app_views.route("/status")
def status():
    """returns status ok"""
    stat = {"status": "ok"}
    return (jsonify(stat))
