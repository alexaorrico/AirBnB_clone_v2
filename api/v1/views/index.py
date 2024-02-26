#!/usr/bin/python3
"""index"""
from flask import Flask, jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def ret_status():
    return jsonify({"status": "OK"})


if __name__ == "__main__":
    pass
