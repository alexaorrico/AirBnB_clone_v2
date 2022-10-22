#!/usr/bin/python3
""" index module """


from api.v1.views import amenity_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.state import State


@amenity_views.route('amenities', strict_slashes=False)
def get_amenities():
    """ returns a list of all the amenities in db """
    amenities = storage.all(Amenity)
    lst = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(lst)


@amenity_views.route('amenities/<amenity_id>', strict_slashes=False)
def get_amenity_with_id_eq_amenity_id(amenity_id):
    """ returns a amenity with id == amenity_id """
    amenity = storage.get(Amenity, amenity_id)
    return jsonify(amenity.to_dict()) if amenity else abort(404)


@amenity_views.route('amenities/<amenity_id>', strict_slashes=False,
                     methods=["DELETE"])
def delete_amenity_with_id_eq_amenity_id(amenity_id):
    """ deletes an amenity with id == amenity_id """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@amenity_views.route('amenities', strict_slashes=False,
                     methods=["POST"])
def create_amenity():
    """ creates a new amenity """
    try:
        data = request.get_json()
    except Exception:
        return jsonify({
            "error": "Not a JSON"
            }), 400
    name = data.get("name")
    if not name:
        return jsonify({
            "error": "Missing name"
            }), 400
    amenity = Amenity(name=name)
    amenity.save()
    return jsonify(
        amenity.to_dict()
        ), 201


@amenity_views.route('amenities/<amenity_id>', strict_slashes=False,
                     methods=["PUT"])
def update_amenity_with_id_eq_amenity_id(amenity_id):
    """ updates a amenity's record """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        return jsonify({
            "error": "Not a JSON"
            }), 400

    amenity_dict = amenity.to_dict()
    dont_update = ["id", "created_at", "updated_at"]
    for skip in dont_update:
        data[skip] = amenity_dict[skip]
    amenity_dict.update(data)
    amenity.delete()
    storage.save()
    updated_amenity = Amenity(**amenity_dict)
    updated_amenity.save()
    return jsonify(
            updated_amenity.to_dict()
            )


@amenity_views.route('states/<state_id>/amenities', strict_slashes=False)
def get_amenities_of_state(state_id):
    """ returns list of amenities associated with state """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(
                [amenity.to_dict() for amenity in state.amenities]
            )
