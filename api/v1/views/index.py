#!/usr/bin/python3
'''creates route on the object app_views and returns json'''
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    '''status - shows status ok'''
    return jsonify({"status": "OK"})
