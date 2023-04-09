#!/usr/bin/python3

from flask import abort, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', methods=['GET'])
def amenities_list():
    """returns all amenities"""

    from models import storage
    from models.amenity import Amenity

    amenities_found = storage.all(Amenity)
    if amenities_found == None:
        abort(404)

    amenities_list = []

    for amenity in amenities_found:
        amenities_list.append(amenities_found.to_dict())

    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenity(amenity_id):
    """returns amenity of id given"""

    from models import storage
    from models.amenity import Amenity

    amenity_found = storage.get(Amenity, amenity_id)
    if amenity_found == None:
        abort(404)

    return jsonify(amenity_found.to_dict()), 201


@app_views.route('/states/amenities', methods=['POST'])
def create_amenities():
    """create an amenity"""
    from flask import request
    from models.amenity import Amenity

    http_request = request.get_json(silent=True)
    if http_request == None:
        return 'Not a JSON', 400
    elif 'name' not in http_request.keys():
        return 'Missing name', 400

    new_amenity = Amenity(**http_request)
    storage.new(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amenity(amenity_id):
    """updates given amenity"""

    from flask import request
    from models.amenity import Amenity

    found_amenity = storage.get(Amenity, amenity_id)

    if found_amenity == None:
        return '', 404

    http_request = request.get_json(silent=True)
    if http_request == None:
        return 'Not a JSON', 400

    for key, values in http_request.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(found_amenity, key, values)

    storage.save()
    return jsonify(found_amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def amenity_delete(amenity_id):
    """DELETE amenity if id is found"""

    from models import storage
    from models.amenity import Amenity

    amenity_found = storage.get(Amenity, amenity_id)
    if amenity_found == None:
        return '{}', 404

    storage.delete(amenity_found)
    storage.save()
    return jsonify({}), 200
