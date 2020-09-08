#!/usr/bin/python3
"""reviews"""
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort
from models import storage
from models.review import Review
from models.place import Place
from models.base_model import BaseModel


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """list all reviews in place"""
    output = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for review in place.reviews:
        output.append(review.to_dict())
    return (jsonify(output))


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def a_review(review_id):
    """list a review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    output = review.to_dict()
    return (jsonify(output))


@app_views.route('/reviews/<review_id>', methods=["GET", "DELETE"],
                 strict_slashes=False)
def del_a_review(review_id):
    """ delete one unique review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    result = make_response(jsonify({}), 200)
    return result
