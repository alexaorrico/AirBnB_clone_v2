#!/usr/bin/python3
""" index """

from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', methods=['GET'])
def statCode():
    """ call storage.close() """
    return jsonify({'status': 'OK'})
