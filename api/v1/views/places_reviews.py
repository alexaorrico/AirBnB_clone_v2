#!/usr/bin/python3
"""
Reviews routes
"""

from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models import storage
from flask import jsonify, abort, request

from models.user import User


@app_views.route('/places/<string:place_id>/reviews', methods=["GET"],
                 strict_slashes=False)
def reviews_by_place(place_id):
    """GET reviews by place id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if place.reviews is None:
        abort(404)
    else:
        reviews = place.reviews
        reviews_list = []
        for review in reviews:
            reviews_list.append(review.to_dict())
    return (jsonify(reviews_list))


@app_views.route('/reviews/<string:review_id>', methods=["GET"],
                 strict_slashes=False)
def review(review_id):
    """GET Review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return (jsonify(review.to_dict()))


@app_views.route('/reviews/<string:review_id>', methods=["DELETE"],
                 strict_slashes=False)
def remove_review(review_id):
    """REMOVE Review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return {}, 200


@app_views.route('/places/<string:place_id>/reviews', methods=["POST"],
                 strict_slashes=False)
def create_review(place_id, strict_slashes=False):
    """CREATE Review for place by id"""
    if request.is_json:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        json_review = request.get_json()
        if json_review.get("user_id") is None:
            abort(400, description="Missing user_id")
        user = storage.get(User, json_review.get("user_id"))
        if user is None:
            abort(404)
        if json_review.get("text") is None:
            abort(400, description="Missing text")

        json_review["place_id"] = place_id
        new_review = Review(**json_review)
        storage.new(new_review)
        storage.save()
        return new_review.to_dict(), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/reviews/<string:review_id>', methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """UPDATE Review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.is_json:
        forbidden = ["id", "user_id", "place_id", "created_at", "updated_at"]
        review_json = request.get_json()
        storage.delete(review)
        for k, v in review_json.items():
            if k not in forbidden:
                setattr(review, k, v)
        storage.new(review)
        storage.save()
        return review.to_dict(), 200
    else:
        abort(400, description="Not a JSON")
