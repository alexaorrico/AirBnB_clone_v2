#!/usr/bin/python3
"""HTTP methods for API"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/reviews/<review_id>', methods=['GET'])
def reviews(review_id):
    """GET method for reviews"""
    obj_review = storage.get("Review", review_id)
    if obj_review is None:
        abort(404)
    else:
        return jsonify(obj_review.to_dict())


@app_views.route('/places/<place_id>/reviews')
def review_pl(place_id=None):
    list_review = []
    obj_place = storage.get("Place", place_id)
    if obj_place is None:
        abort(404)
    else:
        obj_review = storage.all("Review").values()
        for review in obj_review:
            if review.place_id == place_id:
                list_review.append(review.to_dict())
        return jsonify(list_review)


@app_views.route('/reviews/<review_id>', methods=['DELETE', 'PUT'])
def review_del_put(review_id=None):
    """DELETE and PUT method for reviews"""
    obj_review = storage.get("Review", review_id)
    if obj_review is None:
        abort(404)
    if request.method == 'DELETE':
        obj_review.delete()
        storage.save()
        return (jsonify({})), 200
    if request.method == 'PUT':
        do_put = request.get_json()
        if not do_put:
            return jsonify({"error": "Not a JSON"}), 400
        for k, v in do_put.items():
            if (k is not "id" and
                k is not "created_at" and
                k is not "updated_at" and
                k is not "user_id" and
                    k is not "place_id"):
                setattr(obj_review, k, v)
        obj_review.save()
        return jsonify(obj_review.to_dict()), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def review_post(place_id):
    """POST method for reviews"""
    get_place = storage.get("Place", place_id)
    if get_place is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400
    do_post = request.get_json()
    user_id = do_post.get("user_id")
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if 'text' not in do_post.keys():
        return jsonify({"error": "Missing text"}), 400
    """do_post["place_id"] = str(place_id)"""
    new_review = Review(**do_post)
    setattr(new_review, "place_id", place_id)
    """storage.do_post(new_review)"""
    new_review.save()
    return jsonify(new_review.to_dict()), 201
