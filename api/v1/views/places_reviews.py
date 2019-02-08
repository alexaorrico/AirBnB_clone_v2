#!/usr/bin/python3
"""views for reviews"""
from api.v1.views import app_views
from models import storage, review, place, user
from flask import jsonify, abort, request, make_response


@app_views.route('/places/<place_id>/reviews', methods=["GET"])
def return_reviews(place_id):
    """return all city objects"""
    reviews = []
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404)
    for rev in place_obj.reviews:
        reviews.append(rev.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=["GET"])
def return_review(review_id):
    """return single place object"""
    review_obj = storage.get('Review', review_id)
    if review_obj is None:
        abort(404)
    return jsonify(review_obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=["DELETE"])
def delete_review(review_id=None):
    """delete a review"""
    review_obj = storage.get('Review', review_id)
    if review_obj is None:
        abort(404)
    storage.delete(review_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=["POST"])
def add_review(place_id=None):
    """add a review of place"""
    data = request.get_json(silent=True)
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    if data is None:
        abort(400, jsonify({"message": "Not a JSON"}))
    if 'user_id' not in data.keys():
        abort(400, jsonify({"message": "Missing user_id"}))
    if storage.get("User", data.get('user_id')) is None:
        abort(404)
    if data.get('text') is None:
        abort(400, jsonify({"message": "Missing text"}))
    new_review = review.Review(user_id=data.get('user_id'),
                               place_id=place_id,
                               text=data.get('text'))
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=["PUT"])
def update_review(review_id=None):
    """update a review"""
    dic = {}
    list_key = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    obj = storage.get("Review", review_id)
    if obj is None:
        abort(404)
    dic = request.get_json(silent=True)
    if dic is None:
        abort(400, jsonify({"message": "Not a JSON"}))
    for key, value in dic.items():
        if key not in list_key:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
