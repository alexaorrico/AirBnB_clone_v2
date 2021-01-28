#!/usr/bin/python3
"""handles amenity route requests"""
from api.v1.views import app_views
from models import storage
from models.state import Amenity
from flask import jsonify, request, abort


@app_views.route('/amenities', strict_slashes=False, methods=['POST', 'GET'])
@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=[
    'PUT', 'GET', 'DELETE'])
def amenities(amenities_id=None):
    """retrieves list of all amenities or amenities by amenity_id"""
    if amenity_id is None:
        # /amenities GET method
        if request.method == 'GET':
            list_amen = []
            for amenities in storage.all('Amenity').values():
                list_amen.append(state.to_dict())
            return jsonify(list_amen)

        # /amenities POST method
        if request.method == 'POST':
            new_json = request.get_json(silent=True)
            if new_json is None:
                abort(400, 'Not a JSON')
            if 'name' not in new_json:
                abort(400, 'Missing name')
            new = Amenity(**new_json)
            new.save()
            return jsonify(new.to_dict()), 201

    else:
        # /amenities/<amenitiy_id> GET method
        if request.method == 'GET':
            for amenities in storage.all('Amenity').values():
                if amenities.id == amenity_id:
                    return jsonify(amenities.to_dict())
            abort(404)

        # /amenities/<amenity_id> DELETE method
        if request.method == 'DELETE':
            for amenities in storage.all('Amenity').values():
                if amenities.id == amenity_id:
                    amenities.delete()
                    storage.save()
                    return jsonify({}), 200
            abort(404)

        # /amenities/<amenity_id> PUT method
        if request.method == 'PUT':
            for amenities in storage.all('Amenity').values():
                if amenities.id == amenity_id:
                    new_json = request.get_json(silent=True)
                    if new_json is None:
                        abort(400, 'Not a JSON')
                    for k, v in new_json.items():
                        if k not in ['id', 'created_at', 'updated_at']:
                            setattr(amenities, k, v)
                    amenities.save()
                    return jsonify(amenities.to_dict()), 200
            abort(404)
