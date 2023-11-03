#!/usr/bin/python3
''' Index file '''
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats():
    '''return object stats'''
    stat_count = {}
    for key, value in storage.all().items():
        key = key.split('.')[0]
        if key not in stat_count:
            print(storage.count(key))
            stat_count[key] = storage.count(key)

    return jsonify(stat_count)
