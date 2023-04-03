#!/usr/bin/python3
"""Set up routes for apps"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from flask import jsonify


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    stats = {}
    for cls in storage.classes:
        stats[cls] = storage.count(cls)
        return jsonify(stats)
