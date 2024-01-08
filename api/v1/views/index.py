#!/usr/bin/python3
"""has the routes to be used"""
from api.v1.views import app_views
from flask import jsonify
import json


@app_views.route('/status', methods=['GET'])
def get_status():
    response = {
            'status': 'OK'
            }
    formatted_json = json.dumps(response, indent=2)
    print(formatted_json)
    return jsonify(response)
