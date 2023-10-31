#!/usr/bin/python3
'''Places_amenities view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed
from api.v1.views import app_views
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['DELETE', 'POST']
)
def handle_places_amenities(place_id=None, amenity_id=None):
    '''The method handler for the places endpoint.
    '''
    handlers = {
        'GET': get_place_amenities,
        'DELETE': remove_place_amenity,
        'POST': add_place_amenity
    }
    if request.method in handlers:
        return handlers[request.method](place_id, amenity_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_place_amenities(place_id=None, amenity_id=None):
    '''Gets the amenities of a place with the given id.
    '''
    if place_id:
        a_v_place = storage.get(Place, place_id)
        if a_v_place:
            all_amenities = list(map(lambda x: x.to_dict(), a_v_place.amenities))
            return jsonify(all_amenities)
    raise NotFound()


def remove_place_amenity(place_id=None, amenity_id=None):
    '''Removes an amenity with a given id from a place with a given id.
    '''
    if place_id and amenity_id:
        a_v_place = storage.get(Place, place_id)
        if not a_v_place:
            raise NotFound()
        p_amenity = storage.get(Amenity, amenity_id)
        if not p_amenity:
            raise NotFound()
        aplace_amenity_link = list(
            filter(lambda x: x.id == amenity_id, a_v_place.amenities)
        )
        if not aplace_amenity_link:
            raise NotFound()
        if storage_t == 'db':
            amenity_place_link = list(
                filter(lambda x: x.id == place_id, p_amenity.place_amenities)
            )
            if not amenity_place_link:
                raise NotFound()
            a_v_place.amenities.remove(p_amenity)
            a_v_place.save()
            return jsonify({}), 200
        else:
            all_amenity_idx = a_v_place.amenity_ids.index(amenity_id)
            a_v_place.amenity_ids.pop(all_amenity_idx)
            a_v_place.save()
            return jsonify({}), 200
    raise NotFound()


def add_place_amenity(place_id=None, amenity_id=None):
    '''Adds an amenity with a given id to a a_v_place with a given id.
    '''
    if place_id and amenity_id:
        a_v_place = storage.get(Place, place_id)
        if not a_v_place:
            raise NotFound()
        p_amenity = storage.get(Amenity, amenity_id)
        if not p_amenity:
            raise NotFound()
        if storage_t == 'db':
            aplace_amenity_link = list(
                filter(lambda x: x.id == amenity_id, a_v_place.amenities)
            )
            amenity_place_link = list(
                filter(lambda x: x.id == place_id, p_amenity.place_amenities)
            )
            if amenity_place_link and aplace_amenity_link:
                res = p_amenity.to_dict()
                del res['place_amenities']
                return jsonify(res), 200
            a_v_place.amenities.append(p_amenity)
            a_v_place.save()
            res = p_amenity.to_dict()
            del res['place_amenities']
            return jsonify(res), 201
        else:
            if amenity_id in a_v_place.amenity_ids:
                return jsonify(p_amenity.to_dict()), 200
            a_v_place.amenity_ids.push(amenity_id)
            a_v_place.save()
            return jsonify(p_amenity.to_dict()), 201
    raise NotFound()

