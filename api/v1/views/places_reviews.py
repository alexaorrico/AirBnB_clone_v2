#!/usr/bin/python3
"""
module for CRUD Place object
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews_of_place(place_id):
    """ retrieve the list reviews belongs to place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    json_obj = [rev.to_dict() for rev in place.reviews]
    return jsonify(json_obj)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review_by_id(review_id):
    """retrieve review using param id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_review(review_id):
    """ remove review from storage"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """ create new review """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data.get("user_id"))
    if not user:
        abort(404)
    if 'text' not in data:
        abort(400, "Missing text")
    new_data = data.copy()
    new_data["place_id"] = place_id
    obj_review = Review(**new_data)
    obj_review.save()
    return jsonify(obj_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ update review based on review_id"""
    ref_obj_review = storage.get(Review, review_id)
    if not ref_obj_review:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key in data:
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            # ref_obj_state.__dict__[key] = data[key]
            setattr(ref_obj_review, key, data[key])
    storage.save()
    return jsonify(ref_obj_review.to_dict()), 200
