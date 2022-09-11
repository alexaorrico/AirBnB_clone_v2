#!/usr/bin/python3
"""create a file states.py"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/', methods=['GET'], strit_slashes=False)
def states(state_id=None):
	"""handles RESTFul API for State """
	"""if state_id is not None:
		the_state = storage.get()"""
