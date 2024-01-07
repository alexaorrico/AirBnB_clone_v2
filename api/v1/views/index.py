from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns the status of your API"""
    return jsonify({"status": "OK"})
