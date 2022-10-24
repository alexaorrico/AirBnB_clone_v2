#!/usr/bin/python3
"""View for Amenities objects that handles all default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def get_amenities():
    """Create a new view for Amenity objects that
    handles all default RESTFul API actions"""
    if request.method == 'GET':
        return jsonify([value.to_dict() for value in 
                        storage.all('Amenity').values()])

    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400

        new_amenity = Amenity(**post)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201

@app_views.route('/amenities/<string:amenity_id>', 
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_amenity_id(amenity_id):
    amenity = storage.get('Amenity', amenity_id)

    if amenity is None:
            abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict()), 200
    elif request.method == 'DELETE':
        storage.delete('amenity')
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        put = request.get_json()
        if put is None or type(put) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in put.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
                storage.save()
        return jsonify(amenity.to_dict()), 200
