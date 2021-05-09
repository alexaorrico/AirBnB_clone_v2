#!/usr/bin/python3
"""View configuration for Places-Review"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, place
from models.city import City
from models.place import Place
from models.review import Review

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

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def getplaces(review_id=None):
    """Gets a review according with the id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteplaces(review_id=None):
    """Deletes a review according with the id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        review.delete()
        storage.save()
        return jsonify({}), 200