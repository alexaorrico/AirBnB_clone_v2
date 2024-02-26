#!/usr/bin/python3
"""this is the amenities view for the API"""
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
"""HTTP methods allowed for amenities"""


@app_views.route('/amenities', methods=ALLOWED_METHODS)
@app_views.route('/amenities/<amenity_id>', methods=ALLOWED_METHODS)
def handle_states(state_id=None):
    """handles all allowed HTTP methods to amenity(id)."""
    handlers = {
        'GET': get_amenity,
        'DELETE': del_amenity,
        'POST': add_amenity,
        'PUT': update_amenity,
    }
    if request.method in handlers:
        return handlers[request.method](amenity_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_amenity(amenity_id=None):
    """uses the GET method to retrieve an amenity(id) or all amenities."""
    all_amenities = storage.all(Amenity).values()
    if amenity_id:
        unique_amenity = [amenity for amenity in all_amenities if amenity.id == amenity_id]
        if unique_amenity:
            return jsonify(unique_amenity[0].to_dict())
        else:
            raise NotFound()
    else:
        all_amenities_dicts = [amenity.to_dict() for amenity in all_amenities]
        return jsonify(all_amenities_dicts)


def del_amenity(amenity_id=None):
    """uses the DELETE method to delete an amenity(id)."""
    all_amenities = storage.all(Amenity).values()
    unique_amenity = [amenity for amenity in all_amenities if amenity.id == amenity_id]
    if unique_state:
        amenity_to_delete = unique_unique[0]
        storage.delete(amenity_to_delete)
        storage.save()

        return jsonify({}), 200
    raise NotFound()


def add_state(state_id=None):
    """uses the POST method to add a new state"""
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    A
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()),  201


def update_state(state_id=None):
    """uses the PUT method to update state."""
    keys_to_update = ('id', 'created_at', 'updated_at')
    all_states = storage.all(State).values()
    unique_state = [state for state in all_states if state.id == state_id]
    if unique_state:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        for key, value in data.items():
            if key not in keys_to_update:
                setattr(unique_state[0], key, value)

        unique_state[0].save()

        return jsonify(unique_state[0].to_dict()), 200

    raise NotFound()
