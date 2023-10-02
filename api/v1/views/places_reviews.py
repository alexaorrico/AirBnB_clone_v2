#!/usr/bin/python3
"""module to handle requests regarding a Review object"""

from models.place import Place
from models.review import Review
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views
import json
from flask import request, jsonify, abort


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def get_place_reviews(place_id):
    """retrieves list of all Review objs of a Place"""
    response = storage.get(Place, place_id)
    if response is None:
        # CHECK THIS, FAILS BUT RETURNS A STATUS CODE OF 200
        abort(404)

    all_reviews = storage.all(Review)
    list_reviews = []
    for key, value in all_reviews.items():
        if place_id == value.place_id:
            list_reviews.append(value.to_dict())
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review_obj(review_id):
    """deletes a review object"""
    review_to_delete = storage.get(Review, review_id)

    if review_to_delete is None:
        abort(404)

    storage.delete(review_to_delete)
    storage.save()
    return jsonify({}), 200

@app_views.route('/reviews/<review_id>', strict_slashes=False)
def serve_review_id(review_id):
    """Retrives a Review object"""
    # check if the review id exists for a Review obj
    response = storage.get(Review, review_id)

    if response is None:
        abort(404)

    return jsonify(response.to_dict())


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_new_review(place_id):
    """creates a Review object"""

    response = storage.get(Place, place_id)
    if response is None:
        abort(404)  # NOT WORKING (STATUS CODE IS 200)

    if request.headers['Content-Type'] == 'application/json':
        data_entered = request.get_json()
        if data_entered is None:
            # NOT WORKING NEEDS REPAIR !!!!!
            abort(400, description="Not a JSON")
    else:
        abort(400,"Not a JSON")
        # abort(400, description="Content-Type is not application/json")

    # if name not in dict
    if data_entered.get('text') is None:
        abort(400, description="Missing text")

    if data_entered.get('user_id') is None:
        abort(400, description="Missing user_id")

    # check if the entered user_id is not linked to any User object
    user_id_response = storage.get(User, data_entered.get('user_id'))
    if user_id_response is None:
        abort(404)

    new_review = Review(**data_entered)
    setattr(new_review, "place_id", place_id)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review_obj(review_id):
    """updates a Review object"""
    review_to_update = storage.get(Review, review_id)

    if review_to_update is None:
        abort(404)

    if request.headers['Content-Type'] == 'application/json':
        data_entered = request.get_json()
        if data_entered is None:
            # NOT WORKING NEEDS REPAIR !!!!!
            abort(400, description="Not a JSON")
    else:
        abort(400, description="Not a JSON")
        # abort(400, description="Content-Type is not application/json")

    for key, value in data_entered.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review_to_update, key, value)

    storage.save()

    return jsonify(review_to_update.to_dict()), 200