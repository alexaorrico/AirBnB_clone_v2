from api.v1.views import app_views
from flask import jsonify, abort, make_response,request
from flasgger.utils import swag_from
from models import storage
from models.amenity import Amenity

@app_views('/amenities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenity/all_amenities.yml')
def amenities():
    amenities = storage.all(Amenity).values
    amenity_list = []
    
    for amenity in amenities:
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenity/get_amenity.yml', methods=['GET'])
def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/amenity/delete_amenity.yml', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
@swag_from('documentation/amenity/create_amenity.yml', methods=['POST'])
def create_amenity():
    request_data = request.get_json
    if not request_data:
        abort(400, description='Not a JSON')

    if 'name' not in request_data:
        abort(400, description='Missing name')

    amenity = Amenity(**request_data)
    amenity.save()

    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/amenity/update_amenity.yml', methods=['PUT'])
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    request_data = request.get_json
    if not request_data:
        abort(400, description='Not a JSON')

    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in amenity:
        if key not in ignored_keys:
            setattr(amenity, key, value)
    storage.save()

    return make_response(jsonify(amenity.to_dict()), 200)
