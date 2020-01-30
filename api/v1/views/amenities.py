#!/usr/bin/python3
""" Createa  new view for State objects that handle restfulapi"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity
from models.city import City
from models.state import State


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def list_all_amenities():
    """ Retrieves list of all States """
    data = storage.all('Amenity')
    amenities = [v.to_dict() for k, v in data.items()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_specific_amenity(amenity_id):
    """ Retrieves a state object, if not linked, then 404"""
    data = storage.all('Amenity')
    name = 'Amenity.' + amenity_id
    amenity = [v.to_dict() for k, v in data.items() if k == name]
    if len(amenity) != 1:
        abort(404)
    return jsonify(amenity[0])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_specific_amenity(amenity_id):
    """ Deletes a state object, if not linked, then raise 404 error """
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates a state object """
    new_amenity_dict = request.get_json(silent=True)
    if new_amenity_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    new_amenity = Amenity(**new_amenity_dict)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates state instance """
    update_amenity_json = request.get_json(silent=True)
    if update_amenity_json is None:
        return jsonify({'error': 'Not a JSON'}), 400
    amenities = storage.all('Amenity')
    amenity = None
    for a in amenities:
        if amenity_id in a:
            amenity = amenities[a]
    if not amenity:
        abort(404)
    ignore = ['id', 'created_at', 'updated_at']
    for k, v in update_state_json.items():
        if k not in ignore:
            setattr(amenity, k, v)
            storage.save()
    return jsonify(amenity.to_dict())
