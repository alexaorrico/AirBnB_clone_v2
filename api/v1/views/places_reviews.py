#!/usr/bin/python3
"""Views for the Review class: GET, DELETE,  POST, PUT"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews_from_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    objs = []
    for x in place.reviews:
        objs.append(x.to_dict())
    return jsonify(objs)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    user = storage.get(User, request.get_json()["user_id"])
    if not user:
        abort(404)

    if 'text' not in request.get_json():
        abort(400, 'Missing text')

    d = request.get_json()
    d.update({"place_id": place_id})
    d.update({"user_id": d["user_id"]})
    obj = Review(**request.get_json())
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    review.__dict__.update(request.get_json())
    old_dict = review.to_dict()
    storage.delete(review)
    review = Review(**old_dict)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 200
