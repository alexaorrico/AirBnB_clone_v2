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

@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,
                 methods=['GET'])
def get_places(place_id):
    """ Get All places"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.rivews])