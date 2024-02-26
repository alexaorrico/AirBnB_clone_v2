#!/usr/bin/python3
"""index"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def ret_status():
    return jsonify({"status": "OK"})


if __name__ == "__main__":
    app_views.url_map.strict_slashes = False
