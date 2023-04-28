#!/usr/bin/python3
"""creates a new view fro State that handles all Rest Api actions"""
from models import storage
from flask import jsonify
from api.v1.views import app_views
from models.state import State

@app_views.route('/states')
@app_views.route('/states/<state_id>')
def get_state(id):
    """retrieves the list of all state objects"""
