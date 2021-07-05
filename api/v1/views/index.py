#!/usr/bin/python3
'''
'''
from flask import Blueprint, jsonify
from models import storage

def init():
    from api.v1.views import app_views

    @app_views.route('/status')
    def get_status():
        return jsonify({'status': 'OK'})
    
    @app_views.route('/stats')
    def get_stats():
        stats_objs = {}
        for key, value in storage.classes.items():
            count = storage.count(key)
            stats_objs[value] = count    
        return jsonify(stats_objs)
