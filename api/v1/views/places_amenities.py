#!/usr/bin/python3
"""places_amenities view"""
from api.v1.views import app_views
from flask import jsonify, abort


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def get_amenities_by_place(place_id):
    """Retrieves the list of all amenities objects"""
    from models import storage
    from models.place import Place
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    amenity_list = []
    for amenity in place.amenities:
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity_in_place(place_id, amenity_id):
    """Deletes an amenity in place object"""
    from models import storage
    from models.place import Place
    from models.amenity import Amenity
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    for place_amenity in place.amenities:
        if place_amenity.id == amenity_id:
            storage.delete(place_amenity)
            storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def post_amenity_by_place(place_id, amenity_id):
    """Updates a amenity object"""
    from models import storage
    from models.place import Place
    from models.amenity import Amenity

    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    if amenity not in place.amenities:
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
