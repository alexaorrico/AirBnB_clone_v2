#!/usr/bin/python3
"""states view for the API"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest


ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
"""allowed methods for the states endpoint"""


@app_views.route('/states', methods=ALLOWED_METHODS)
@app_views.route('/states/<state_id>', methods=ALLOWED_METHODS)
def handle_state(state_id=None):
    """handles the states endpoint"""

    handlers = {
        'GET': get_states,
        'POST': add_states,
        'DELETE': rm_states,
        'PUT': update_state,
    }
    
    if request.method in handlers:
        return handlers[request.method](state_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))
    
def get_states(state_id=None):
    """
    gets the state with the given ID or all states
    """
    all_states = storage.all(State).values()
    if state_id:
        result = list(filter(lambda x: x.id == state_id, all_states))
        if result:
            return jsonify(result[0].to_dict())
        raise NotFound
    all_states = list(map(lambda x: x.to_dict(), all_states))