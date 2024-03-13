#!/usr/bin/python3
""" Place Reviews Module """

from api.v1.views import app_views
from flask import abort, Flask, jsonify, make_response
from models.place import place_amenity, Place
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get(place_id):
    """ Returns a list of Reviews objects """
    place_obj = storage.get(Place, place_id)
    if place_obj:
        all_reviews = storage.all(Review)
        reviews = []
        for obj in all_reviews.values():
            if obj.place_id == place_id:
                reviews.append(obj.to_dict())
        return make_response(jsonify(reviews), 200)
    abort(404)


@app_views.route('/reviews/<review_id>', )
