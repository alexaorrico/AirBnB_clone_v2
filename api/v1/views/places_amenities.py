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
    if place_id:
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        else:
            if request.method == 'GET':
                amenity_list = []
                if storage_t == 'db':
                    # DBStorage: list, create and delete Amenity
                    for amenity in place.amenities:
                        amenity_list.append(amenity.to_dict())
                    return jsonify(amenity_list)
                else:
                    # FileStorage: list, add and remove Amenity
                    amenity_list = place.amenity_ids
                    return jsonify(amenity_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST', 'DELETE'],
                 strict_slashes=False)
def handles_post_delete_amenity(place_id=None, amenity_id=None):
    """Deletes a Amenity object to a Place and
       Link a Amenity object to a Place (post).
       uses the '/places/<place_id>/amenities/<amenity_id>' route
    """
    if place_id and amenity_id:
        place = storage.get(Place, place_id)
        amenity = storage.get(Amenity, amenity_id)
        if not place or not amenity:
            abort(404)
        else:
            if storage_t == 'db':
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
            else:
                if request.method == 'DELETE':
                    place.amenity_ids.remove(amenity.id)
                    storage.save()
                    return jsonify({}), 200
                elif request.method == 'POST':
                    for am_id in place.amenity_ids:
                        if am_id == amenity.id:
                            return jsonify({"amenity_id": am_id}), 200
                    place.amenity_ids.append(amenity.id)
                    storage.save()
                    return jsonify({"amenity_id": amenity.id}), 201
