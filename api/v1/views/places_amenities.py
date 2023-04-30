#!/usr/bin/python3
"""creates a new view for Amenity that handles all Rest Api actions"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models import storage_t
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def handles_get_amenities(place_id=None):
    """Retrieves the list of all amenity objects by place
       uses the '/places/<place_id>/amenities' places routes
    """
    if storage_t == 'db':
        if place_id:
            place = storage.get(Place, place_id)
            if not place:
                abort(404)
            else:
                if request.method == 'GET':
                    amenity_list = []
                    for amenity in place.amenities:
                        amenity_list.append(amenity.to_dict())
                    return jsonify(amenity_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST', 'DELETE'],
                 strict_slashes=False)
def handles_post_delete_amenity(place_id=None, amenity_id=None):
    """Deletes a Amenity object to a Place and
       Link a Amenity object to a Place (post).
       uses the '/places/<place_id>/amenities/<amenity_id>' route
    """
    if storage_t == 'db':
        if place_id and amenity_id:
            place = storage.get(Place, place_id)
            amenity = storage.get(Amenity, amenity_id)
            if not place or not amenity:
                abort(404)
            else:
                if request.method == 'DELETE':
                    storage.delete(amenity)
                    storage.save()
                    return jsonify({}), 200
                elif request.method == 'POST':
                    for item in place.amenities:
                        if item.id == amenity.id:
                            return jsonify(item.to_dict()), 200
                    place.amenities.append(amenity)
                    storage.save()
                    return jsonify(amenity.to_dict()), 201
