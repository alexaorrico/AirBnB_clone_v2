#!/usr/bin/python3
"""function to create the route status"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews')
def reviews(place_id):
    """get reviews with his place_id"""
    for val in storage.all("Place").values():
        if val.id == place_id:
            return jsonify(list(map(lambda v: v.to_dict(), val.reviews)))
    abort(404)


@app_views.route('/reviews/<review_id>')
def review_id(review_id):
    """get review with his id"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def reviews_delete(review_id):
    """delete a obj with his id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    storage.close()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def review_create(place_id):
    """create review object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
    else:
        msg = "Not a JSON"
        return jsonify({"error": msg}), 400

    if "user_id" not in data:
        msg = "Missing user_id"
        return jsonify({"error": msg}), 400

    user = storage.get("User", data["user_id"])
    if user is None:
        abort(404)

    if "text" not in data:
        msg = "Missing text"
        return jsonify({"error": msg}), 400

    data.update({'place_id': place_id})
    review = Review(**data)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def review_update(review_id):
    """update review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
    else:
        msg = "Not a JSON"
        return jsonify({"error": msg}), 400

    for k, v in data.items():
        if k not in ["id", "created_at", "updated_at",
                     "place_id", "user_id"]:
            setattr(review, k, v)

    storage.save()
    return jsonify(review.to_dict()), 200
