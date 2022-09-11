#!/usr/bin/python3
"""create a file index.py"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Status"""
    new_dict = {}
    new_dict['status'] = "OK"
    return jsonify(new_dict)

@app_views.route('/stats')
def stats():
	"""with count we ring number of object"""
	objs_count = {}
	objs_count['states'] = storage.count("State")
	
	return jsonify(objs_count)
