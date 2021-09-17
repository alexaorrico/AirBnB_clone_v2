#!/uar/bin/python3
"""Is the Status of your API dile"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", methods=["GET"])
def status():
    """"Function that return a JSON dictionary"""
    return jsonify({"status": "OK"})
