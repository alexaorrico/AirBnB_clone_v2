#!/usr/bin/python3
"""states"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_placereview(place_id=None):
    """take reviews from each place"""
    if storage.get(Place, place_id) is None:
        abort(404)
    placereview = []
    for pr in storage.get(Place, place_id).reviews:
        placereview.append(pr.to_dict())
    return jsonify(placereview)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id=None):
    """get review object"""
    if storage.get(Review, review_id) is None:
        abort(404)
    else:
        return jsonify(storage.get(Review, review_id).to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_review(review_id=None):
    """delete review object"""
    if storage.get(Review, review_id):
        storage.delete(storage.get(Review, review_id))
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """add review object"""
    if storage.get(Place, place_id) is None:
        abort(404)
    if request.get_json() is None:
        abort(400, "Not a JSON")
    elif "user_id" not in request.get_json().keys():
        abort(400, "Missing user_id")
    elif not storage.get("User", request.get_json()["user_id"]):
        abort(404)
    elif "text" not in request.get_json().keys():
        abort(400, "Missing text")
    else:
        new_review = Review(**request.get_json())
        new_review.place_id = place_id
        storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id=None):
    """change review object"""
    if storage.get("Review", review_id) is None:
        abort(404)
    if request.get_json() is None:
        return "Not a JSON", 400
    for key, value in request.get_json().items():
        if key in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            pass
        else:
            setattr(storage.get("Review", review_id), key, value)
    storage.save()
    return jsonify(storage.get("Review", review_id).to_dict()), 200
