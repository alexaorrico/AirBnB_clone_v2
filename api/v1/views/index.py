#!/usr/bin/python3
'''creating an index route'''
from flask import Flask, jsonify, Response
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def return_status():
    '''returns the status fo the method'''
    stat = Response(status=200)
    return jsonify({"status": f"{stat}"})


@app_views.route('/stats', methods=['GET'])
def return_stats():
    '''returns a count of the instances of a class'''
    new_dict = {}
    # query all classes and
    # return a count of the instances of the class in storage
