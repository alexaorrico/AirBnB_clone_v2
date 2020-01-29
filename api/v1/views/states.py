#!/usr/bin/python3
"""
Handles all default RESTful API actions for State objects
"""

from . import app_views
from models.state import State
from flask.json import jsonify
from models import storage


@app_views.route("/states", methods=['GET'])
def states():
    """Retrieves the list of all State objects"""
    return jsonify([state.to_dict() for state in storage.all('State').values()])

# @app_views.route("/states/<state_id>", methods=('GET', 'POST'))
