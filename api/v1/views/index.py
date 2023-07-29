from flask.json import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def get_status():
    """Return server status"""
    return jsonify({"status": "OK"}), 200
