#!/usr/bin/python3
'''
'''
from flask import Blueprint, jsonify


def init():
    from api.v1.views import app_views

    @app_views.route('/status')
    def get_status():
        return jsonify({'status': 'OK'})
