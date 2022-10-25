#!/usr/bin/python3
"""Create a new view for review objects that handles all default RESTFul API
actions"""

from api.v1.views import app_views
from flask import request, abort, jsonify
from models.review import Review
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieves get method for all reviews"""
    for place in storage.all(Place).values():
        if place.id == place_id:
            list_r = []
            for review in place.reviews:
                list_r.append(review.to_dict())
            return jsonify(list_r)
    return abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def reviewsWithId(review_id):
    """Methods that retrieves all methods for reviews with id"""
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)

    if request.method == 'GET':
        """Retrieves a review of a given review_id"""
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        """Deletes a review of a given review_id"""
        review.delete()
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        """Update an review of a given review_id"""
        r = request.get_json()
        if r is None:
            return abort(400, 'Not a JSON')
        toIgnore = ["id", "created_at", "updated_it", "user_id", "place_id"]
        for key, value in r.items():
            if key not in toIgnore:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict())


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def post_review(place_id):
    """Create a new review"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    r = request.get_json()
    if r is None:
        abort(400, "Not a JSON")
    if r.get("user_id") is None:
        abort(400, "Missing user_id")
    user = storage.get(User, r['user_id'])
    if user is None:
        return abort(404)
    if r.get("text") is None:
        abort(400, "Missing text")
    r['place_id'] = place_id
    new = Review(**r)
    new.save()
    return jsonify(new.to_dict()), 201
