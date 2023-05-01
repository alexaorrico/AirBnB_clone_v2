#!/usr/bin/python3
'''Handles all default RESTFul API actions for Review objects'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route(
        '/places/<place_id>/reviews',
        methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    '''retrieves the list of all Review objects of a Place'''

    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    reviews_list = [review.to_dict() for review in place_obj.reviews]
    return jsonify(reviews_list)


@app_views.route(
        '/reviews/<review_id>',
        methods=['GET'], strict_slashes=False)
def get_review(review_id):
    '''retrieves a Review object'''

    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        abort(404)

    review_dict = review_obj.to_dict()
    return jsonify(review_dict)


@app_views.route(
        '/reviews/<review_id>',
        methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    '''deletes a Review object'''

    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        abort(404)

    storage.delete(review_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/reviews',
        methods=['POST'], strict_slashes=False)
def create_review(place_id):
    '''creates a Review object'''

    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    json_data = request.get_json()
    if json_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'user_id' not in json_data.keys():
        return jsonify({"error": "Missing user_id"}), 400
    elif 'text' not in json_data.keys():
        return jsonify({"error": "Missing text"}), 400

    user_obj = storage.get(User, json_data['user_id'])
    if user_obj is None:
        abort(404)

    new_obj = Review(place_id=place_id, **json_data)
    new_obj.save()

    return jsonify(new_obj.to_dict()), 201


@app_views.route(
        '/reviews/<review_id>',
        methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''updates a Review object'''

    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        abort(404)

    json_data = request.get_json()
    if json_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for attr, val in json_data.items():
        if attr not in [
                'id', 'user_id',
                'place_id', 'created_at',
                'updated_at']:
            setattr(review_obj, attr, val)
    review_obj.save()

    return jsonify(review_obj.to_dict()), 200
