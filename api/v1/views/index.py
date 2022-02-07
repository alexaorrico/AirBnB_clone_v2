#!/usr/bin/python3
""" This a index file"""
from flask import Flask, jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Valid method of objects """
    num_obj = {}
    for key, value in classes.items():
        num_obj[value] = storage.count(key)
    return jsonify(num_obj)
