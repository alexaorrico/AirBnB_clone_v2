from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """returning a json string"""
    return jsonify({"status": "OK"})

# @app_views.route('/stats')
# def method_name():
#     pass