#!/usr/bin/python3
"""
View for Reviews that handles all RESTful API action
"""

from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews_all(place_id):
    """ returns list of all Review objects """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="place_id not linked to any Place object")
    reviews_all = []
    reviews = storage.all(Review).values()
    for review in reviews:
        if review.place_id == place_id:
            reviews_all.append(review.to_dict())
    return jsonify(reviews_all)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def review_get(review_id):
    """ handles GET method """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404, description="review_id not linked to any Review object")
    review = review.to_dict()
    return jsonify(review)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_delete(review_id):
    """ handles DELETE method """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404, description="review_id not linked to any Review object")
    storage.delete(review)
    storage.save()
    response = make_response(jsonify({}), 200)
    return response


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_post(place_id):
    """ handles POST method """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="place_id not linked to any Place object")
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404, description="user_id not linked to any User object")
    if 'text' not in data:
        return make_response(jsonify({"error": "text"}), 400)
    new_review = Review(**data)
    new_review.place_id = place_id
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def review_put(review_id):
    """ handles PUT method """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404, description="city_id not linked to any City object")
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in data.items():
        ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
