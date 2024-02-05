#!/usr/bin/python3
"""a module as places reviews API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def get_places_review(place_id):
    """a function to retrieve all reviews of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>")
def get_place_review(review_id):
    """a function to get a review of a place by review_id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'])
def delete_place_review(review_id):
    """a function to delete a review of a place object by review_id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def post_place_review(place_id):
    """a function to create a new review of a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    try:
        json_req = request.get_json()
    except Exception:
        json_req = None

    if not json_req:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in json_req:
        return jsonify({"error": "Missing user_id"}), 400

    user_id = json_req['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if 'text' not in json_req:
        return jsonify({"error": "Missing text"}), 400

    review = Review(**json_req)
    review.place_id = place_id
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'])
def update_place_review(review_id):
    """a function to update a review of a place object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    try:
        json_req = request.get_json()
    except Exception:
        json_req = None

    if not json_req:
        return jsonify({"error": "Not a JSON"}), 400

    ignored_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in json_req.items():
        if key not in ignored_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
