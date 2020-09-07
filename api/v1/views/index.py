#!/usr/bin/python3
"""[a script to route /status on the object app_views]
"""
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """[status route]

    Returns:
        [json]: [json status]
    """
    return jsonify({"status": "ok"})
