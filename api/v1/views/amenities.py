#!/usr/bin/python3
"""
States file for APi project
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def list_amenities():
    """lists all amenities"""
    s_list = []
    amenities = storage.all("Amenity")
    for amenity in amenities.values():
        print(amenity.name, amenity.id)
        s_list.append(amenity.to_dict())
    return jsonify(s_list)


@app_views.route('/amenity/<amenity_id>', methods=['GET'])
def GetAmenityById(amenity_id):
    """Retrieves amenity based on its id for GET HTTP method"""
    all_amenity = storage.all("Amenity")
    for amenity in all_amenity.values():
        if amenity.id == amenity_id:
            return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenity/<amenity_id>', methods=['DELETE'])
def DeleteAmenityById(amenity_id):
    """Deletes an amenity based on its id for DELETE HTTP method"""
    amenities = storage.all('Amenity')
    s_id = "Amenity." + amenity_id
    to_del = amenities.get(s_id)
    if to_del is None:
        abort(404)
    storage.delete(to_del)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def PostAmenity():
    """Posts a amenity"""
    info = request.get_json()
    if not info:
        abort(400, 'Not a JSON')
    elif "name" not in info:
        abort(400, 'Missing name')
    amenity = Amenity()
    amenity.name = info['name']
    amenity.save()
    amenity = amenity.to_dict()
    return jsonify(amenity), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def PutAmenity(amenity_id):
    """ Updates a Amenity uses PUT HTTP method"""
    exists = False
    all_states = storage.all("Amenity")
    for amenity in all_states.values():
        if amenity.id == amenity_id:
            exists = True
    if not exists:
        abort(404)
    info = request.get_json()
    if not info:
        abort(400, 'Not a JSON')
    upt_state = all_states['{}.{}'.format('Amenity', amenity_id)]
    upt_state.name = info['name']
    upt_state.save()
    upt_state = upt_state.to_dict()
    return jsonify(upt_state), 200


if __name__ == '__main__':
    pass
