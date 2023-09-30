#!/usr/bin/python3
'''Contains the amenities view for the API.'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates a new Amenity object """

    # if body doesn't contain valid JSON
    if not request.is_json:
        abort(400, "Not a JSON")

    # else transform HTTP body into a dict
    body = request.get_json()

    # if the name key doesnt exist in the body dict
    if body.get("name") is None:
        abort(400, "Missing name")

    # create and save the new amenity instance
    new_amenity = Amenity(**body)
    storage.new(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def retrieve_amenities():
    """ Retrieves a list of all Amenity objects """
    # grab all amenity objects from storage
    amenities = storage.all(Amenity).values()

    # convert all amenity objects into dictionaries & put in list
    amenity_list = [amenity.to_dict() for amenity in amenities]

    # return the jsonified list
    return jsonify(amenity_list)


@app_views.route('/amenities/<id>', methods=['GET'], strict_slashes=False)
def retrieve_amenity(id):
    """ Retrieves a single Amenity object based on its id """
    # grab the amenity object from storage
    amenity = storage.get(Amenity, id)

    if amenity:  # return the jsonified object
        return jsonify(amenity.to_dict())
    else:  # else if amenity is None
        abort(404)


@app_views.route('/amenities/<id>', methods=['PUT'], strict_slashes=False)
def update_amenity(id):
    """ Updates specific instance of an Amenity object """
    # retrieve the object by id if it exists
    amenity = storage.get(Amenity, id)

    # abort if amenity with specific id can't be found
    if amenity is None:
        abort(404)

    # if body doesn't contain valid JSON
    if not request.is_json:
        abort(400, "Not a JSON")

    # else transform HTTP body into a dict
    body = request.get_json()

    # ignore id, created_at, updated_at keys during update
    excluded_keys = ["id", "created_at", "updated_at"]
    # iterate over body dict & update the amenity object
    # with the new values from body dict
    for key, value in body.items():
        if key not in excluded_keys:
            setattr(amenity, key, value)

    # save the updated amenity instance
    storage.save()

    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(id):
    """ Deletes specific instance of an Amenity object """
    # retrieve the object by id if it exists
    amenity = storage.get(Amenity, id)

    # delete the object if it exists
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:  # else if amenity is None
        abort(404)
