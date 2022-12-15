#!/usr/bin/python3
"""
    Module index to app web framework
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    '''
        return Dic of OK status
    '''
    return jsonify({'status': 'OK'})
