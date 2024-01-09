#!/usr/bin/python3

"""Place-Amenity relationship view."""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity

app = Flask(__name__)


@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_amenities(place_id):
    """Get all Amenity objects of a Place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:  # FileStorage
        amenity_ids = place.amenity_ids
        amenities = [storage.get(Amenity, amenity_id).to_dict() for amenity_id in amenity_ids]

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """Delete an Amenity object from a Place."""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        if amenity not in place.amenities:
            abort(404)

        place.amenities.remove(amenity)
    else:  # FileStorage
        if amenity_id not in place.amenity_ids:
            abort(404)

        place.amenity_ids.remove(amenity_id)

    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """Link an Amenity object to a Place."""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200

        place.amenities.append(amenity)
    else:  # FileStorage
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200

        place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201

