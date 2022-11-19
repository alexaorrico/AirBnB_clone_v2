from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'])
def status_okay():
    """
    Returns 200: Status Okay
    """
    return jsonify({"status" : "OK"})