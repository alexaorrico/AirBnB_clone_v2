#!/usr/bin/python3
"""creates a new view for amenitiese that handles all Rest Api actions"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def get_amenity(amenity_id=None):
    """retrieves the list of all amenity objects"""
    amenities = storage.all(Amenity)
    if not amenity_id:
        # uses the '/amenities/ routes
        if request.method == 'GET':
            amenity_list = []
            for amenity in amenities.values():
                amenity_list.append(amenity.to_dict())
            return jsonify(amenity_list)
        elif request.method == 'POST':
            data = request.get_json()
            if not data:
                abort(400, 'Not a JSON')
            if not data.get('name'):
                abort(400, 'Missing name')
            new_obj = Amenity(**data)
            new_obj.save()
            return jsonify(new_obj.to_dict()), 201
    else:
        # uses the '/amenities/<amenity_id>' route
        amenity_obj = storage.get(Amenity, amenity_id)
        if not amenity_obj:
            abort(404)
        if request.method == 'GET':
            return jsonify(amenity_obj.to_dict())
        elif request.method == 'DELETE':
            storage.delete(amenity_obj)
            storage.save()
            return jsonify({}), 200
        elif request.method == 'PUT':
            data = request.get_json()
            if not data:
                abort(400, 'Not a JSON')
            amenity_obj.name = data.get('name')
            amenity_obj.save()
            return jsonify(amenity_obj.to_dict()), 200
