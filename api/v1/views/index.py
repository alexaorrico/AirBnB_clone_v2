#!/usr/bin/python3
''' Creating Flask App route'''


from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/status')
def app_viewsRoute():
    '''doing json things for status'''
    jStatus = {'status': 'OK'}
    return jsonify(jStatus)
