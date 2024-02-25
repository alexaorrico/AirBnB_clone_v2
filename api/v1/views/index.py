from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """ returns a JSON message"""
    return jsonify(status="OK")