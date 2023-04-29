#!/usr/bin/python3

from flask import jsonify

@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'OK'})
