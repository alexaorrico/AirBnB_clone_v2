from api.v1.views import app_views
import models
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def get_amenities(place_id):
    """get all amenities in a place"""
    if models.storage_t == 'db':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = []
        for amenity in storage.all(Amenity).values():
            if amenity.place_id == place_id:
                amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(place_id, amenity_id):
    """get an amenity"""
    if models.storage_t == 'db':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        for amenity in place.amenities:
            if amenity.id == amenity_id:
                return jsonify(amenity.to_dict())
        abort(404)
    else:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None or amenity.place_id != place_id:
            abort(404)
        return jsonify(amenity.to_dict())
    

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """delete an amenity"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for amenity in place.amenities:
        if amenity.id == amenity_id:
            amenity.delete()
            storage.save()
            return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def create_amenity(place_id, amenity_id):
    """create an amenity"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    amenity = Amenity(**request.get_json())
    amenity.place_id = place_id
    amenity.save()
    return jsonify(amenity.to_dict()), 201


