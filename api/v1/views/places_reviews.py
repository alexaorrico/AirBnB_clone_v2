#!/usr/bin/python3
""" module that implements the review api """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_reviews(place_id):
    """ gets all review objects per place using the place_id """
    my_place = storage.get("Place", place_id)
    if not my_place:
        abort(404)
    return jsonify([review.to_dict() for review in my_place.reviews])
