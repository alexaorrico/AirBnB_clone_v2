#!/usr/bin/python3
""" script for views """

from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort
from flask import request, make_response


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """Route that returns all reviews"""
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)

    all_list = []
    for review in place_obj.reviews:
        all_list.append(review.to_dict())

    return make_response(jsonify(all_list), 200)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """Route that returns a review by its ID"""
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)

    return make_response(jsonify(review_obj.to_dict()), 200)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_delete(review_id):
    """ delete http request"""
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)
    storage.delete(review_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_post(place_id):
    """post http request """
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")
    if 'user_id' not in request.json:
        abort(400, description="Missing user_id")
    if 'text' not in request.json:
        abort(400, description="Missing text")

    request_dict = request.get_json()
    user_id = request_dict['user_id']
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)

    obj = Review()
    request_dict['place_id'] = place_id

    for k, v in request_dict.items():
        setattr(obj, k, v)

    # add obj to current DB session and save it.
    storage.new(obj)
    storage.save()
    new_state = obj.to_dict()
    return make_response(jsonify(new_state), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def review_update(review_id):
    """put http request"""
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    new_dict = request.get_json()
    ignore_keys = {'id', 'user_id', 'place_id', 'created_at', 'updated_at'}
    for k, v in new_dict.items():
        if k not in ignore_keys:
            setattr(review_obj, k, v)

    storage.save()
    return make_response(jsonify(review_obj.to_dict()), 200)
