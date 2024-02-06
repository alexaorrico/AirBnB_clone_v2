#!/usr/bin/python3
"""
Define route for view amenity
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.amenity import Amenity
from models import storage, storage_t


@app_views.route('/places/<string:place_id>/amenities', strict_slashes=False)
@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 strict_slashes=False, methods=['DELETE', 'POST'])
def amenities_place(place_id=None, amenity_id=None):
    """Retrieves amentiy or All the amenities given place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if amenity_id is None:
        amenities = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities)

    amentiy = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.method == 'DELETE':
        for place_amentiy in place.amenities:
            if place_amentiy.id == amentiy.id:
                if storage_t == 'db':
                    place.amenities.remove(amentiy)
                else:
                    place.amentiy_id.remove(amentiy.id)

            storage.save()
            return jsonify({})
        abort(404)

    if request.method == 'POST':
        for place_amentiy in place.amenities:
            if place_amentiy.id == amentiy.id:
                return jsonify(amentiy.to_dict())

        if storage_t == 'db':
            place.amenities.append(amentiy)
        else:
            place.amentiy_id.append(amentiy.id)
        return jsonify(amenity.to_dict()), 201
