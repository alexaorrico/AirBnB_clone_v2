from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def check_status():
    """
    returns the status
    """
    return jsonify({"status": "OK"})
