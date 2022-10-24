#!/usr/bin/python3

"""Module to handle place_review request Blueprint"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """return json array of all reviews of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    return jsonify([val.to_dict() for val in reviews])


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a new place review"""
    if storage.get(Place, place_id) is None:
        abort(404)
    if request.get_json():
        body = request.get_json()
    else:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in body:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if storage.get(User, body["user_id"]) is None:
        abort(404)
    if "text" not in body:
        return make_response(jsonify({"error": "Missing text"}), 400)
    body["place_id"] = place_id
    new_review = Review(**body)
    new_review.save()
    if storage.get(Review, new_review.id) is not None:
        return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Method to get a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete a single review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """update properties of a single review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.get_json():
        body = request.get_json()
    else:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    _exceptions = ["id", "created_at", "updated_at", "place_id", "user_id"]
    for k, v in body.items():
        if k not in _exceptions:
            setattr(review, k, v)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
