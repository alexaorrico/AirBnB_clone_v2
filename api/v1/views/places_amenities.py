#!/usr/bin/python3
"""places_amenities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    # Routes for DBStorage
    @app_views.route('/places/<place_id>/amenities', methods=['GET'])
    @app_views.route('/places/<place_id>/amenities/', methods=['GET'])
    def list_amenities_of_place(place_id):
        ''' Retrieves a list of all Amenity objects of a Place '''
        place = storage.get(Place, place_id)
        if not place:
            abort(404)

        return jsonify([amenity.to_dict() for amenity in place.amenities])

    @app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
    def create_place_amenity(place_id, amenity_id):
        '''Creates a Amenity'''
        place = storage.get(Place, place_id)
        amenity = storage.get(Amenity, amenity_id)
        if not place or not amenity:
            abort(404)

        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200

        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201

    @app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
    def delete_place_amenity(place_id, amenity_id):
        '''Deletes a Amenity object from a Place'''
        place = storage.get(Place, place_id)
        amenity = storage.get(Amenity, amenity_id)
        if not place or not amenity:
            abort(404)

        if amenity not in place.amenities:
            abort(404)

        place.amenities.remove(amenity)
        storage.save()
        return jsonify({}), 200

else:
    # Routes for FileStorage
    @app_views.route('/places/<place_id>/amenities', methods=['GET'])
    @app_views.route('/places/<place_id>/amenities/', methods=['GET'])
    def list_amenities_of_place(place_id):
        ''' Retrieves a list of all Amenity objects of a Place '''
        place = storage.get(Place, place_id)
        if not place:
            abort(404)

        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]
        return jsonify(amenities)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
    def create_place_amenity(place_id, amenity_id):
        '''Creates a Amenity'''
        place = storage.get(Place, place_id)
        amenity = storage.get(Amenity, amenity_id)
        if not place or not amenity:
            abort(404)

        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200

        place.amenity_ids.append(amenity_id)
        storage.save()
        return jsonify(amenity.to_dict()), 201

    @app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
    def delete_place_amenity(place_id, amenity_id):
        '''Deletes a Amenity object from a Place'''
        place = storage.get(Place, place_id)
        amenity = storage.get(Amenity, amenity_id)
        if not place or not amenity:
            abort(404)

        if amenity_id not in place.amenity_ids:
            abort(404)

        place.amenity_ids.remove(amenity_id)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_place_amenity(amenity_id):
    '''Retrieves a Amenity object'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())
