#!/usr/bin/python3
"""module that defines app_view func"""
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route("/status")
def status():
    status = {
        "status": "OK"
    }

    return jsonify(status)
