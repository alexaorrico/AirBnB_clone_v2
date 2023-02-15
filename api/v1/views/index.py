from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Returns status in JSON Format"""
    return jsonify({"status": "OK"})
