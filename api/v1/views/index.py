#!/usr/bin/python3
"""
index.py
"""
from . import app_views
from flask import Flask, jsonify


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})
