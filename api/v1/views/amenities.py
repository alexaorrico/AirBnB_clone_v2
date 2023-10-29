#!/usr/bin/python3
"""Module containing views for Amenity objects """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenity objects

    Returns:
        A list of dictionaries representing Amenity Objects in JSON format.
    """
    amenities = []
    for amenity in storage.all("Amenity").values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id=None):
    """ Retrieves a amenity object by amenity_id

        Args:
            amenity_id (str): The UUID4 string representing a Amenity object.

        Returns:
            A amenity object in JSON format.
            Raise 404 error if no match for amenity_id is found.
    """
    if amenity_id:
        for amenity in storage.all("Amenity").values():
            if amenity.id == amenity_id:
                return jsonify(amenity.to_dict())
        abort(404)


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id=None):
    """ Deletes a amenity object by amenity_id

        Args:
            amenity_id (str): The UUID4 string representing a Amenity object.

        Returns:
            An empty dictionary with the status code 200.
            Raise 404 error if no match for amenity_id is found.
    """
    amenity_obj = storage.get("Amenity", amenity_id)
    if amenity_obj is None:
        abort(404)
    amenity_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates a amenity object

        Returns:
            A dictionary of the amenity object with status code 201.
            If HTTP body request is not valid JSON, raise a 400 error with the
                message "Not a JSON".
            If dictionary doesn't contain the key name, raise a 400 error with
                message "Missing name".
    """
    if request.json is None:
        return "Not a JSON", 400
    fields = request.get_json()
    if fields.get('name') is None:
        return "Missing name", 400
    new_amenity = Amenity(**fields)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id=None):
    """ Updates a amenity object by amenity_id

        Args:
            amenity_id (str): The UUID4 string representing a Amenity object.

        Returns:
            A amenity object in JSON format with the status code 200.
            If no object with matching amenity_id is found,
                404 error is raised.
            If HTTP body request is not valid JSON, raise a 400 error with the
                message "Not a JSON".
            If dictionary doesn't contain the key name, raise a 400 error with
                message "Missing name".
    """
    if request.json is None:
        return "Not a JSON", 400
    fields = request.get_json()
    amenity_obj = storage.get("Amenity", amenity_id)
    if amenity_obj is None:
        abort(404)
    for key in fields:
        if key not in ['id', 'created_at', 'updated_at']:
            if hasattr(amenity_obj, key):
                setattr(amenity_obj, key, fields[key])
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 200
