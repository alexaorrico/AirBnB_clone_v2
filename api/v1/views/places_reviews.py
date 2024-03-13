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
        for key, value in all_reviews.items():
            
    abort(404)
