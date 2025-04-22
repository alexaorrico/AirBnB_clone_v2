#!/usr/bin/python3
"""sets up restful actions for amenities model"""
from api.v1.views import amenities_views
from flask import jsonify as js, request
from models.amenity import Amenity
from models import storage


@amenities_views.route('/amenities', methods=['GET'])
def list_of_amenities():
    """retrieves the list of all Amenity objects"""
    try:
        amenities = storage.all(Amenity)
        return js([amenity.to_dict() for amenity in amenities.values()])
    except Exception as e:
        return js({"error": "{}".format(e)})


@amenities_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """retrieves an amenity associated with the amenity id"""
    try:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            return js(amenity.to_dict())
        return js({"error": "Amenity object does not exist"}), 404
    except Exception as e:
        return js({"error": "{}".format(e)})


@amenities_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """deletes an amenity if exists"""
    try:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            storage.delete(amenity)
            storage.save()
            return {}, 200
        return js({"error": "Amenity object does not exist"}), 404
    except Exception as e:
        return js({"error": "{}".format(e)})


@amenities_views.route('/amenities', methods=['POST'])
def create_amenity():
    """creates an Amenity object"""
    # check for a JSON
    if not request.is_json:
        return js({"error": "Not a JSON"}), 400
    # fetch data
    try:
        request_info = request.get_json()
        # check if name key exists
        if "name" not in request_info.keys():
            return js({"error": "Missing name"}), 400
        # create an Amenity object
        new_amenity = Amenity(name=request_info.get("name"))
        storage.save()
        return js(new_amenity.to_dict())
    except Exception as e:
        return js({"": "{an error occured}".format(e)})


@amenities_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """updates an amenity if exists"""
    # fetch amenity associated with amenity_id
    amenity = storage.get(Amenity, amenity_id)
    # check if amenity_id exists
    if amenity:
        try:
            # check for a valid JSON
            if not request.is_json:
                return js({"error": "Not a JSON"}), 400
            request_info = request.get_json()
            # attrs not to be updated
            attrs_to_ignore = ["id", "created_at", "updated_at"]
            for attr, value in request_info.items():
                if attr not in attrs_to_ignore:
                    amenity.__setattr__(attr, value)
            storage.save()
            return js(amenity.to_dict()), 201
        except Exception as e:
            return js({"": "{an error occured}".format(e)})
    # amenity does not exist
    return js({"error": "Amenity object does not exist"})
