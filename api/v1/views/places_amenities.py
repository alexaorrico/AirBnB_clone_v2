
#!/usr/bin/python3
"""
places
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from os import environ
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def get_amenities_places(place_id):

    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404, 'Not found')
    if STORAGE_TYPE == 'db':
        
        place_amenities = place_obj.amenities
       
    else:
        place_amen_ids = place_obj.amenities
        place_amenities = []
        for amen in place_amen_ids:
            place_amenities.append(storage.get('Amenity', amen))
    place_amenities = [
        obj.to_dict() for obj in place_amenities
    ]
    return jsonify(place_amenities)

@app_views.route('/places/<place_id>/amenities/<amenitie_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenities_places(place_id, amenitie_id):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404, 'Not found')
    amenitie = storage.get('Amenitie', amenitie_id)
    if amenitie is None:
        abort(404)
    if amenitie_id in place.amenities:
        abort(404)
    if STORAGE_TYPE == 'db':
        storage.delete(amenitie)
        storage.save()
    else:
        del place.amenity_ids[amenitie_id]

        
    return jsonify({}),200
    

    




