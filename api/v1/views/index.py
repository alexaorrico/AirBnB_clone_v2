'''index module'''
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status_check():
    """Returns the status of the app"""
    return jsonify({"status": "OK"})
