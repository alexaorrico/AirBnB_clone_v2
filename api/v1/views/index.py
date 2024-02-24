from api.v1.views import app_views
from flask import jsonify, make_response


@app_views.route('/status')
def status():
    """Gives status 200 message"""
    return make_response(jsonify({"status": "OK"}), 200)