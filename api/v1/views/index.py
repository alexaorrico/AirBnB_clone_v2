#!/usr/bin/python3

"""  views index module """

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def api_status():
    return jsonify({"status": "OK"})
