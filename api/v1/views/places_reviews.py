#!/usr/bin/python3
"""View configuration for Places-Review"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, place
from models.city import City
from models.place import Place

@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Gets all reviwes depending of place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    res = []
    for i in city.reviews:
        res.append(i.to_dict())
    return jsonify(res)

