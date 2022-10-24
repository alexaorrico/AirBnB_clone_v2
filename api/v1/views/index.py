#!/usr/bin/python3
"""index module showing status end-point"""


from api.v1.views import app_views
from flask import jsonify
import json


@app_views.route('/status')
def show_status():
    return jsonify({"status": "OK"})
