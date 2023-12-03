#!/usr/bin/python3
""" Handles everything related to reviews """

from models import storage
from models.review import Review
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route("/places/<place_id>/reviews", methods=['GET'])
def get_review_by_place(place_id):
    """Retrieves all reviews by place id"""
    get_p = storage.get("Place", place_id)
    if not get_p:
        abort(404)
    return jsonify([r.to_dict() for r in get_p.reviews])


@app_views.route("/reviews/<review_id>", methods=['GET'])
def get_review_by_id(review_id):
    """
    Reyrieves a review by id
    """
    instance = storage.get("Review", review_id)
    if not instance:
        abort(404)
    return jsonify(instance.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """
    Delete a review with the given id
    """
    instance = storage.get("Review", review_id)
    if not instance:
        abort(404)
    storage.delete(instance)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_new_review(place_id):
    """
    Create a new review
    """
    get_p = storage.get("Place", place_id)
    if not get_p:
        abort(404)
    res = request.get_json()
    if res is None:
        abort(400, 'Not a JSON')
    if 'text' not in res:
        abort(400, 'Missing text')
    if 'user_id' not in res:
        abort(400, 'Missing user_id')
    get_u = storage.get("User", res['user_id'])
    if not get_u:
        abort(404)
    instance = Review(**res)
    instance.user_id = res['user_id']
    instance.place_id = place_id
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_review_by_id(review_id):
    """
    Update an review with the given id
    """
    instance = storage.get("Review", review_id)
    if not instance:
        abort(404)
    res = request.get_json()
    if res is None:
        abort(400, 'Not a JSON')
    if 'text' in res:
        instance.text = res['text']
    if 'place_id' in res:
        get_p = storage.get("Place", res['place_id'])
        if not get_p:
            abort(404)
        instance.place_id = res['place_id']
    if 'user_id' in res:
        get_u = storage.get("User", res['user_id'])
        if not get_u:
            abort(404)
        instance.user_id = res['user_id']
    instance.save()
    return jsonify(instance.to_dict()), 200
