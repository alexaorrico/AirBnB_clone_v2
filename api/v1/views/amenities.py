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
def handle_amenities(amenity_id=None):
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
        unique_amenity = [amenity for amenity in all_amenities
                          if amenity.id == amenity_id]
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
    unique_amenity = [amenity for amenity in all_amenities
                      if amenity.id == amenity_id]
    if unique_amenity:
        amenity_to_delete = unique_amenity[0]
        storage.delete(amenity_to_delete)
        storage.save()

        return jsonify({}), 200
    raise NotFound()


def add_amenity(amenity_id=None):
    """uses the POST method to add a new Amenity."""
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')

    if 'name' not in data:
        raise BadRequest(description='Missing name')
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()),  201


def update_amenity(amenity_id=None):
    """uses the PUT method to update amenity."""
    keys_to_update = ('id', 'created_at', 'updated_at')
    all_amenities = storage.all(Amenties).values()
    upd_amenity = [amenity for amenity in all_amenities
                   if amenity.id == amenity_id]
    if upd_amenity:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        for key, value in data.items():
            if key not in keys_to_update:
                setattr(upd_amenity[0], key, value)

        upd_amenity[0].save()

        return jsonify(upd_amenity[0].to_dict()), 200

    raise NotFound()
