from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """This methos returns the status of API"""
    return jsonify({"status": "OK"})
