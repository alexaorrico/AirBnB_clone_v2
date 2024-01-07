#!/usr/bin/python3
'''
contains the following routes:
/states is used for creating a new state or getting all states
/states/<state_id> for getting, updating or deleting a single state
'''
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest


ROUTE_METHODS = ['GET', 'DELETE', 'POST', 'PUT']

@app_views.route('/states', methods=ROUTE_METHODS)
@app_views.route('/states/<state_id>', methods=ROUTE_METHODS)
def handle_state_routes(state_id=None):
    ''' handles all valid routes '''
    handlers = {
        'GET': _get,
        'DELETE': _delete,
        'POST': _add,
        'PUT': _update,
    }
    if request.method in handlers:
        return handlers[request.method](state_id)
        
    raise MethodNotAllowed(list(handlers.keys()))


def _get(state_id=None):
    ''' get state when id is given else return all states '''
    all_states = storage.all(State).values()

    if state_id:
        filtered_states = list(filter(lambda x: x.id == state_id, all_states))
        if filtered_states is None or len(filtered_states) < 1:
            raise NotFound()
        return jsonify(filtered_states[0].to_dict())

    all_states = list(map(lambda x: x.to_dict(), all_states))

    return jsonify(all_states)


def _delete(state_id=None):
    '''Removes a state with the given id.
    '''
    all_states = storage.all(State).values()
    filtered_states = list(filter(lambda x: x.id == state_id, all_states))
    if filtered_states:
        storage.delete(filtered_states[0])
        storage.save()
        return jsonify({}), 200

    raise NotFound()


def _add(state_id=None):
    '''Adds a new state.
    '''
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    new_state = State(**data)
    new_state.save()

    return jsonify(new_state.to_dict()), 201


def _update(state_id=None):
    '''Updates the state with the given id.
    '''
    xkeys = ('id', 'created_at', 'updated_at')
    all_states = storage.all(State).values()
    filtered_states = list(filter(lambda x: x.id == state_id, all_states))
    if filtered_states is None or len(filtered_states) < 1:
        raise NotFound()
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    old_state = filtered_states[0]
    for key, value in data.items():
        if key not in xkeys:
            setattr(old_state, key, value)
    old_state.save()

    return jsonify(old_state.to_dict()), 200
