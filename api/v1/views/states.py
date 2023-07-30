#!/usr/bin/python3
"""Create a new view for State objects that
handles all default RESTFul API actions"""
from flask import jsonify
from api.v1.views import app_views
from models.state import State
from models import storage

classes = {"State": State}


@app_views.route('/states')
def view_states():
    """List all states"""
