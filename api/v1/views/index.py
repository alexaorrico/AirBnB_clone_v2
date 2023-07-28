from . import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    return jsonify({"status": "OK"})
