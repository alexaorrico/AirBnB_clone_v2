#!/usr/bin/python3
"""
Define route for view Amenity
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities/<string:amenity_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
@app_views.route('/amenities', strict_slashes=False, methods=['GET', 'POST'])
def amenities(amenity_id=None):
    """Retrieves a Amenity or All the amenities"""
    if request.method == 'GET':
        if amenity_id is not None:
            amenity = storage.get(Amenity, amenity_id)
            if amenity is None:
                abort(404)
            return jsonify(amenity.to_dict())
        amenities = storage.all(Amenity)
        amenities_dicts = [val.to_dict() for val in amenities.values()]
        return jsonify(amenities_dicts)

    elif request.method == 'DELETE':
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        elif 'name' not in data:
            return make_response(jsonify({'error': 'Missing name'}), 400)
        else:
            amenity = Amenity(**data)
            amenity.save()
            return make_response(jsonify(amenity.to_dict()), 201)

    elif request.method == 'PUT':
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)

        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'not a json'}), 400)

        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return make_response(jsonify(amenity.to_dict()), 200)
