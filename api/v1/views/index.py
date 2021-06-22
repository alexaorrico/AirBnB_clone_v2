#!/usr/bin/python3
""" creating app route"""
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status')
def app_views_route():
    """ jsonify our code"""
    return jsonify({"status": "OK"})
