#!/usr/bin/python3
"""view for Review objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def place_reviews(place_id):
    """Retrieves the list of all Review objects based on the place_id"""
    place = storage.get(Place, place_id)

    if place:
        reviews = place.reviews
        reviews_list = []
        for review in reviews:
            reviews_list.append(review.to_dict())
        return jsonify(reviews_list)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a place based on it's ID"""
    review = storage.get(Review, review_id)

    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review based on it's ID"""
    review = storage.get(Review, review_id)

    if review:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def add_review(place_id):
    """Adds a review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    if 'text' not in data:
        abort(400, description="Missing text")
    new_review = Review(**data)
    new_review.place_id = place.id
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """updates a review"""
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    ignore_list = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_list:
            setattr(review, key, value)
        else:
            pass

    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
