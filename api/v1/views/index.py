#!/usr/bin/python3
"""
Flask routes and returns json status reponse
"""
from flask import Flask, jsonify, request
from api.v1.views import app_views


@app_views.route("/status", methods=["GET"])
def status():
    """Function for the status of the route"""
    if method == "GET":
        return jsonify({"status": "OK"})

