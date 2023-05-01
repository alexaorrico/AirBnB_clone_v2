#!/usr/bin/python3
"""route /amenities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Method that retrieve a list of all amenities by id"""
    all_amenities = storage.all(Amenity).values()
    result = [amenity.to_dict() for amenity in all_amenities]

    return jsonify(result)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """Retrieves a Amenity object: GET /api/v1/amenities/id"""
    amenity = storage.get(Amenity, amenity_id)
    if (amenity is None):
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """ delete a resource of my list of states """

    delete_amenity = storage.get(Amenity, amenity_id)
    if delete_amenity is None:
        abort(404)
    else:
        storage.delete(delete_amenity)
        storage.save()
        return (jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_new_amenity():
    """ create new resource by my list of amenities """

    amenity_object_json = request.get_json()
    if amenity_object_json is None:
        return (jsonify({'Error': 'Not a JSON'}), 400)

    if 'name' not in amenity_object_json.keys():
        return (jsonify({'Error': 'Missing name'}), 400)

    amenity_object = Amenity(**amenity_object_json)
    amenity_object.save()
    return jsonify(amenity_object.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_a_amenity(amenity_id=None):
    """ update a resource of my objects """

    amenity_object_json = request.get_json()
    if amenity_object_json is None:
        return jsonify({'Error': 'Not a JSON'}), 400

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        ignore = ['id', 'created_at', 'updated_at']
        for key, value in amenity_object_json.items():
            if key not in ignore:
                setattr(amenity, key, value)
            else:
                pass
        amenity.save()

    return (jsonify(amenity.to_dict()), 200)
