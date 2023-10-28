#!/usr/bin/python3
"""handles all defaults RESTful API actions for reviews"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def get_review(place_id):
    """retrieves all reviews of a given place"""
    place = storage.get(Place, place_id)
    if place:
        reviews = storage.all(Review)
        review_list = []

        for review in reviews.values():
            if review.place_id == place_id:
                review_list.append(review.to_dict())
        return jsonify(review_list)
    abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_review_id(review_id):
    """retrieves a review based on a given id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes a review based on its id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """creates a new review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    if "text" not in data:
        return abort(400, "Missing text")
    if "user_id" not in data:
        return abort(400, "Missing user_id")
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    review = Review()
    review.place_id = place_id
    review.user_id = data["user_id"]
    review.text = data["text"]
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """updates a given review"""
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "user_id",
                       "place_id"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
