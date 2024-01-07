from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', method=['GET'])
def status():
    """returning a json string"""
    return jsonify({"status": "OK"})