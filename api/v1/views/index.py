#!/usr/bin/python3

from api.v1.views import app_views
from flask import Blueprint, jsonify

@app_view.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'ok'})
