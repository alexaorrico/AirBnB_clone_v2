#!/usr/bin/python3
"""
Creates a view for Review objects that Handles all default RESTFul API
actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """
   Returns all reviews for a place based on id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)


    obj_list = []
    all_objs = storage.all(Review)
    for obj in all_obj.values():
        if obj.place_id == place_id:
            obj_list.append(obj.to_dict())
    return jsonify(obj_list), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_reviews(place_id):
    """
    Creates a new review for a place based on place id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    elif 'user_id' not in data.keys():
        abort(400, 'Missing user_id')
    elif 'text' not in data.keys():
        abort(400, 'Missing text')

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    obj = Review(place_id=place_id, **data)
    storage.new(obj)
    storage.save()

    return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def method_reviews(review_id):
    """
    Retrieves a review based on it's id
    """
    review = storage.get(Review, review_id)
    if review is None or not review:
        abort(404)

    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def method_reviews(review_id):
    """
    Deletes a review based on it's id
    """
    review = storage.get(Review, review_id)
    if review is None or not review:
        abort(404)

    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def method_reviews(review_id):
    """
    Updates a review based on its id
    """
    review = storage.get(Review, review_id)
    if review is None or not review:
        abort(404)


    data = request.get_json()
    if not data:
        abort(404, "Not a JSON")

    skip = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
    for key, value in data.items():
    if key not in skip:
        setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
