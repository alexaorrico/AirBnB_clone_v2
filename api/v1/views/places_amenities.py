from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route(
    '/places/<place_id>/amenities', methods=['GET'], strict_slashes=False
)
def get_amenities_objs(place_id):
    '''Retrieves the list of all Amenity objects of a Place'''
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify(error="Not found"), 404

    if storage.__class__.__name__ == 'DBStorage':
        place_amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        place_amenities = [storage.get(
            Amenity, amenity_id).to_dict() for amenity_id in place.amenity_ids]

    return jsonify(place_amenities)


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['DELETE'], strict_slashes=False
)
def delete_amenity_from_place(place_id, amenity_id):
    '''Deletes an Amenity object from a Place'''
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        return jsonify(error="Not found"), 404

    if storage.__class__.__name__ == 'DBStorage':
        if amenity in place.amenities:
            place.amenities.remove(amenity)
        else:
            return jsonify(error="Not found"), 404
    else:
        if amenity_id in place.amenity_ids:
            place.amenity_ids.remove(amenity_id)
        else:
            return jsonify(error="Not found"), 404

    storage.save()
    return jsonify({})


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['POST'], strict_slashes=False
)
def link_amenity_to_place(place_id, amenity_id):
    '''Link an Amenity object to a Place'''
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        return jsonify(error="Not found"), 404

    if storage.__class__.__name__ == 'DBStorage':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
